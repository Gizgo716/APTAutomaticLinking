from AlternativesGenerator import AltGen
from ChainGenerator import ChainGen

print ("Finding Alternatives...")
generator1 = AltGen
generator1.run()
print("Alternatives found")
generator2 = ChainGen()
combinationCount = generator2.prepare()
while True:
    response = input(f"Do you want to find all {combinationCount} chains? (y/n): ")
    if response.lower() in ("yes", "y"):
        
        generator2.combine()
        break
    elif response.lower() in ("no", "n"):
        print("Exiting.")
        break


