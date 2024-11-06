import subprocess

wordlist = "./rockyou.txt"

hashes = [
    "./hashes/hashes_weak.txt",
    "./hashes/hashes_moderate.txt",
    "./hashes/hashes_strong.txt"
]

output = [
    "./cracked_combined/cracked_weak.txt",
    "./cracked_combined/cracked_moderate.txt",
    "./cracked_combined/cracked_strong.txt"
]

def main():
    for i in range(3):
        hashcat_command = [
            'hashcat',
            '-m', '0',                   # MD5 mode
            '-a', '1',                   # Attack mode 1 (combinator)
            '-O',                        # Optimize for speed
            '--workload-profile', '4',   # Workload profile
            '-o', output[i],             # Output file for cracked hashes
            hashes[i],                   # Hash file
            wordlist,                    # First wordlist
            wordlist                     # Second wordlist
        ]
         
        subprocess.Popen(
            hashcat_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).wait()

        show_command = [
            'hashcat',
            '-m', '0',        # MD5 mode
            '--show',         # Show cracked hashes and passwords
            hashes[i]         # Hash file
        ]

        show_process = subprocess.Popen(
            show_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )

        cracked_hashes = show_process.communicate()[0]

        password_list = [
            line.split(':', 1)[1] if ':' in line else ''
            for line in cracked_hashes.strip().split('\n') 
            if line
        ]

        with open(output[i], 'w') as f_out:
            f_out.write(str(password_list))

if __name__ == "__main__":
    main()