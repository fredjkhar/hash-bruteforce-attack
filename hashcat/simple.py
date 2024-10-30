import subprocess

wordlist = "./rockyou.txt"

hashes = ["./hashes/hashes_weak.txt",
           "./hashes/hashes_moderate.txt",
           "./hashes/hashes_strong.txt"]

output = ["./cracked/cracked_weak.txt",
            "./cracked/cracked_moderate.txt",
            "./cracked/cracked_strong.txt"]

def main():
        for i in range(3):
            hashcat_command = [
                'hashcat',          # Command
                '-m', '0',          # Hash type: 0 for MD5
                '-a', '0',          # Attack mode: 0 for dictionary attack
                '-o', output[i],  # Temporary output file
                hashes[i],          # Input hash file
                wordlist            # Wordlist file
            ]
             
            process = subprocess.Popen(
                hashcat_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Read output line by line
            for line in process.stdout:
                print(line, end='')  # Print Hashcat's output in real-time
            
            # Wait for the process to complete
            process.wait()

            # Define the Hashcat command for showing cracked hashes
            show_command = [
                'hashcat',
                '-m', '0',
                '--show',
                hashes[i]
            ]

            # Execute the show command
            show_process = subprocess.Popen(
                show_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            cracked_hashes = ""

            # Read and capture output
            for line in show_process.stdout:
                cracked_hashes += line

            # Write cracked hashes to the output file
            with open(output[i], 'w') as f_out:
                f_out.write(cracked_hashes)

            # Wait for the process to complete
            show_process.wait()

if __name__ == "__main__":
    main()