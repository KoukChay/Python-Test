global point
global name
global money

try:
    c_pointa = int(input("%-30s: " % "Enter amount of point you want to change<1point = $5>"))
    if point >= c_pointa:
        point -= c_pointa
        money += (c_pointa * 5)
        print(f'Congratulation! You own now ${money}')

        sms = f"up:{money}:{point}:{name}".encode('utf-8')
        client = self.run_client()
        client.send(sms)
        self.profile_page(r_data)
    else:
        print("Not enough point to change money.")

except ValueError:
    print("Amount must be only Numbers!")