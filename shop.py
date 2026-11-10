# 상품 클래스
class Product:
    count = 1  # 상품 번호 카운트

    def __init__(self, name, price, stock):
        self.id = Product.count
        Product.count += 1
        self.name = name
        self.price = price
        self.stock = stock

    def sold_out(self):
        return self.stock == 0  # 남은 재고 0 일 경우 True, 아니면 False 리턴

    def reduce_stock(self, amount):
        if self.stock >= amount:
            self.stock -= amount
            return True
        return False


# 할인 쿠폰 클래스
class Discount:
    def __init__(self, name="쿠폰 없음"):
        self.name = name

    def calculate(self, total_price):
        return 0


class RateDiscount(Discount):
    def __init__(self, name, rate=0.1, max_amount=5000):
        super().__init__(name)
        self.rate = rate
        self.max_amount = max_amount

    def calculate(self, total_price):
        discount = int(total_price * self.rate)
        if discount > self.max_amount:
            return self.max_amount
        else:
            return discount


class FixedDiscount(Discount):
    def __init__(self, name, amount=3000, min_total=20000):
        super().__init__(name)
        self.amount = amount
        self.min_total = min_total

    def calculate(self, total_price):
        if total_price >= self.min_total:
            return self.amount
        return 0


# 장바구니 클래스
class Cart:
    def __init__(self):
        self.items = {}
        self.coupon = Discount()

    def add_item(self, product, amount):
        if product in self.items:
            self.items[product] += amount
        else:
            self.items[product] = amount

    def remove_item(self, product):
        if product in self.items:
            del self.items[product]

    def clear(self):
        self.items.clear()
        self.coupon = Discount()

    def get_summary(self):
        total_price = 0
        for product in self.items:
            count = self.items[product]
            total_price += product.price * count

        discount_amount = self.coupon.calculate(total_price)

        # 배송비 계산
        if total_price == 0:
            delivery_fee = 0
        elif (total_price - discount_amount) >= 30000:
            delivery_fee = 0
        else:
            delivery_fee = 3000

        final_price = total_price - discount_amount + delivery_fee
        return total_price, discount_amount, delivery_fee, final_price


# 쇼핑몰 메인
class Shop:
    def __init__(self):
        self.products = [
            Product("무선 이어폰", 89000, 3),
            Product("텀블러", 15000, 10),
            Product("보조배터리", 32000, 5),
            Product("마우스패드", 9000, 0),
            Product("USB 허브", 18000, 4),
        ]

        self.coupons = [
            Discount("쿠폰 없음"),
            RateDiscount("10% 할인 (최대 5000원)", rate=0.1, max_amount=5000),
            FixedDiscount("3000원 할인 (20000원 이상 구매 시)", amount=3000, min_total=20000),
        ]
        self.cart = Cart()

    def run(self):
        while True:
            print("\n------------------------------")
            print("1. 상품목록  2. 담기  3. 빼기  4. 장바구니  5. 쿠폰  6. 결제  q. 종료")
            print("------------------------------")
            choice = input("선택 : ")

            if choice == "1":
                self.show_products()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.remove_from_cart()
            elif choice == "4":
                self.show_cart()
            elif choice == "5":
                self.select_coupon()
            elif choice == "6":
                self.checkout()
            elif choice == "q":
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다.")

    # 1. 상품 목록 보여주기
    def show_products(self):
        print("\n[상품 목록]")
        for product in self.products:
            if product.sold_out():
                print(str(product.id) + ". " + product.name + " (" + str(product.price) + "원) - 품절")
            else:
                print(str(product.id) + ". " + product.name + " (" + str(product.price) + "원) - 재고: " + str(product.stock) + "개")

    # 2. 장바구니에 담기
    def add_to_cart(self):
        self.show_products()
        number = int(input("\n담을 상품 번호 : "))

        if number < 1 or number > 5:
            print("없는 상품 번호입니다.")
            return

        selected_product = self.products[number - 1]

        if selected_product.sold_out():
            print("품절된 상품입니다.")
            return

        amount = int(input("담을 수량 : "))
        if amount <= 0:
            print("1개 이상 담아야 합니다.")
            return

        already_in_cart = 0
        if selected_product in self.cart.items:
            already_in_cart = self.cart.items[selected_product]

        if already_in_cart + amount > selected_product.stock:
            print("재고가 부족합니다! (남은 재고: " + str(selected_product.stock) + "개, 장바구니에 담긴 수량: " + str(already_in_cart) + "개)")
            return

        self.cart.add_item(selected_product, amount)
        print(selected_product.name + " 상품을 장바구니에 담았습니다.")

    # 3. 장바구니에서 빼기
    def remove_from_cart(self):
        if self.cart.items == {}:
            print("\n장바구니가 비어 있습니다.")
            return

        print("\n[내 장바구니]")
        for product in self.cart.items:
            print(str(product.id) + ". " + product.name)

        number = int(input("\n빼낼 상품 번호 : "))

        for product in self.cart.items:
            if product.id == number:
                self.cart.remove_item(product)
                print(product.name + " 상품을 뺐습니다.")
                return

        print("장바구니에 없는 상품입니다.")

    # 4. 내 장바구니 보기
    def show_cart(self):
        print("\n[장바구니 내역]")
        if self.cart.items == {}:
            print("장바구니가 비어 있습니다.")
            return

        for product in self.cart.items:
            count = self.cart.items[product]
            price_sum = product.price * count
            print("- " + product.name + " " + str(count) + "개 : " + str(price_sum) + "원")

        total, discount, delivery, final_price = self.cart.get_summary()
        print("------------------------------")
        print("적용 쿠폰 : " + self.cart.coupon.name)
        print("주문 금액 : " + str(total) + "원")
        print("할인 금액 : -" + str(discount) + "원")
        print("배 송 비  : +" + str(delivery) + "원")
        print("최종 금액 : " + str(final_price) + "원")

    # 5. 쿠폰 선택하기
    def select_coupon(self):
        print("\n[쿠폰 목록]")
        print("1. 쿠폰 없음")
        print("2. 10% 할인 (최대 5000원)")
        print("3. 3000원 할인 (20000원 이상 구매 시)")

        number = int(input("\n적용할 쿠폰 번호 : "))

        if number == 1:
            self.cart.coupon = self.coupons[0]
            print("쿠폰 없음이 적용되었습니다.")
        elif number == 2:
            self.cart.coupon = self.coupons[1]
            print("10% 할인 쿠폰이 적용되었습니다.")
        elif number == 3:
            self.cart.coupon = self.coupons[2]
            print("3000원 할인 쿠폰이 적용되었습니다.")
        else:
            print("없는 쿠폰 번호입니다.")

    # 6. 결제하기
    def checkout(self):
        if self.cart.items == {}:
            print("\n장바구니가 비어 있습니다.")
            return

        self.show_cart()
        ans = input("\n결제하시겠습니까? (y/n) : ")
        if ans == "y":

            for product in self.cart.items:
                count = self.cart.items[product]
                product.reduce_stock(count)

            print("\n결제가 완료되었습니다!")
            self.cart.clear()

            self.show_products()
        else:
            print("결제를 취소했습니다.")

shop = Shop()
shop.run()