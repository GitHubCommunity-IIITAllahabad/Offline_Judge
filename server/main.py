import gen
import export
import head
import server
import encode
import delete

print("Offline Judge (Server)")
print("1. Generate Server's key-pair")
print("2. Export Server's public-key")
print("3. Generate head.txt")
print('4. Encode test files')
print("5. Run the server")
print("6. Cleanup server")
print("7. Exit")

opt = input("Enter selection: ")

if opt == str(1):
	gen.main()
elif opt == str(2):
	export.main()
elif opt == str(3):
	head.main()
elif opt == str(4):
	encode.main()
elif opt == str(5):
    server.main()
elif opt == str(6):
    delete.main()
