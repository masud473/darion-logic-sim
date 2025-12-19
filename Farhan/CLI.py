import Backend as base

def menu():
    while True:
        print("\n--- Circuit Simulator Menu ---")
        print("1. Add Component")
        print("2. List Components")
        print("3. Connect Components")
        print("4. Disconnect Components")
        print("5. Set Input Variable Value")
        print("6. Show Output of a Component")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            base.addComponent()
        elif choice == '2':
            base.listComponent()
        elif choice == '3':
            base.listComponent()
            gate_code = input("Enter the serial of the gate you want to connect components: ")
            gate_code=base.complist[int(gate_code)]
            childlist = list(map(int,input("Enter the serial of the component to connect to: ").split()))
            for child in childlist:
                base.connect(gate_code, base.complist[child])
                print(f"Connected {base.complist[child]} to {gate_code}.")

        elif choice == '4':
            base.listComponent()
            gate_code = input("Enter the serial of the gate you want to disconnect components: ")
            gate_code=base.complist[int(gate_code)]
            childlist = list(map(int,input("Enter the serial of the component to disconnect to: ").split()))
            for child in childlist:
                base.disconnect(gate_code, base.complist[child])
                print(f"Disconnected {base.complist[child]} to {gate_code}.")

        elif choice == '5':
            base.listVar()
            var = input("Enter the code of the variable to set : ")
            if var in base.varlist:
                value = input("Enter the value (0 or 1): ")
                if value in ['0', '1']:
                    base.connect(var, value)
                    print(f"Variable {var} set to {value}.")
                else:
                    print("Invalid value. Please enter 0 or 1.")

        elif choice == '6':
            base.listComponent()
            gate_code = input("Enter the serial of the gate you want to see output of: ")
            gate_code=base.complist[int(gate_code)]
            base.output(gate_code)
           
        elif choice == '7':
            print("Exiting Circuit Simulator.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
