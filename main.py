class DeliveryBiker:

    def __init__(self, identifier: str, fixed_price: float):
        self.identifier = identifier
        self.fixed_price = fixed_price
        self.current_deliveries_qtd = 0
        self.exclusive_stores = []

    def register_exclusive_stores(self, store_identifier):
        self.exclusive_stores.append(store_identifier)


class Store:

    def __init__(self, identifier: str, bonus_to_delivery: float):
        self.identifier = identifier
        self.bonus_to_delivery = bonus_to_delivery
        self.priority_bikers = []

    def register_priority_bikers(self, biker_identifier):
        self.priority_bikers.append(biker_identifier)


class Order:

    def __init__(self, store: Store, price: float):
        self.store = store
        self.price = price
        self.delivery_biker: DeliveryBiker = None

    def calculate_bonus_to_delivery(self):
        return (self.price * self.store.bonus_to_delivery) / 100

    def set_delivery_biker(self, delivery_biker: DeliveryBiker):
        self.delivery_biker = delivery_biker


class OrderDispatcher:

    @staticmethod
    def orchestrator(bikers: [DeliveryBiker], orders: [Order]):
        max_per_biker = len(orders) / len(bikers)
        for idx, order in enumerate(orders):
            priority = [b for b in order.store.priority_bikers
                        if b.current_deliveries_qtd < max_per_biker
                        or idx == len(orders) - 1]
            if len(priority) > 0:
                biker = priority[0]
                order.delivery_biker = biker
                biker.current_deliveries_qtd += 1
                continue

            available_bikers = [b for b in bikers
                                if b.current_deliveries_qtd < max_per_biker
                                and (order.store in b.exclusive_stores
                                     or len(b.exclusive_stores) == 0)]
            if len(available_bikers) > 0:
                biker = available_bikers[0]

            order.delivery_biker = biker
            biker.current_deliveries_qtd += 1


if __name__ == '__main__':
    moto1 = DeliveryBiker('MOTO1', 2.0)
    moto2 = DeliveryBiker('MOTO2', 2.0)
    moto3 = DeliveryBiker('MOTO3', 2.0)
    moto4 = DeliveryBiker('MOTO4', 2.0)
    moto5 = DeliveryBiker('MOTO5', 3.0)
    bikers_to_dispatcher = [
        moto1,
        moto2,
        moto3,
        moto4,
        moto5
    ]

    store1 = Store('STORE1', 5.0)
    store2 = Store('STORE2', 5.0)
    store3 = Store('STORE3', 15.0)
    store1.register_priority_bikers(moto4)
    moto4.register_exclusive_stores(store1)

    orders_to_dispatcher = [
        Order(store1, 50.0),
        Order(store1, 50.0),
        Order(store1, 50.0),
        Order(store2, 50.0),
        Order(store2, 50.0),
        Order(store2, 50.0),
        Order(store2, 50.0),
        Order(store3, 50.0),
        Order(store3, 50.0),
        Order(store3, 100.0)
    ]

    OrderDispatcher.orchestrator(bikers_to_dispatcher, orders_to_dispatcher)

    while True:
        for b in bikers_to_dispatcher:
            print("Digite " + b.identifier + " para visualizar pedidos desse Motoboy")
        print("Digite 'GERAL' pra visualizar o relatório geral")
        print("Digite 'SAIR' pra encerrar a iteração")
        escolha_usuario = (input().upper())
        if len([m for m in bikers_to_dispatcher if m.identifier == escolha_usuario]):
            print("ESCOLHEU " + escolha_usuario)
            print("------------------------------------------------")
            orders_of_choose = [o for o in orders_to_dispatcher if o.delivery_biker.identifier == escolha_usuario]
            print("Quantidade de pedidos: " + str(len(orders_of_choose)))
            print("")
            for o in orders_of_choose:
                print("Valor do pedido: " + str(o.price))
                print("Loja do pedido: " + str(o.store.identifier))
                print("Valor total da corrida: " + str(o.delivery_biker.fixed_price + o.calculate_bonus_to_delivery()))
                print("------------------------------------------------")
            print("")
        elif escolha_usuario == 'GERAL':
            for b in bikers_to_dispatcher:
                print("MOTO " + b.identifier)
                print("------------------------------------------------")
                orders_of_choose = [o for o in orders_to_dispatcher if o.delivery_biker.identifier == b.identifier]
                print("Quantidade de pedidos: " + str(len(orders_of_choose)))
                print("")
                for o in orders_of_choose:
                    print("Valor do pedido: " + str(o.price))
                    print("Loja do pedido: " + str(o.store.identifier))
                    print("Valor total da corrida: " + str(
                        o.delivery_biker.fixed_price + o.calculate_bonus_to_delivery()))
                    print("------------------------------------------------")
                print("")
        elif escolha_usuario == 'SAIR':
            quit()
        else:
            print("Escolha inválida!")
