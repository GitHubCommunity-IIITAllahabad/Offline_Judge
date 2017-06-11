import gen
import export
import genhash
import server
import encode

print("Offline Judge (Server)")
print("1. Generate Server's key-pair")
print("2. Export Server's public-key")
print("3. Generate hashes.txt")
print('4. Encode test files')
print("5. Run the server")
print("6. Exit")

opt = input("Enter selection: ")

if opt == str(1):
	gen.main()
elif opt == str(2):
	export.main()
elif opt == str(3):
	genhash.main()
elif opt == str(4):
	encode.main()
elif opt == str(5):
	server.main()
