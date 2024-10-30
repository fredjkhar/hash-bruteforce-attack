import subprocess

wordlist = "./rockyou.txt"
rule_file = "./rules/best64.rule"

hashes = ["./hashes/hashes_weak.txt",
          "./hashes/hashes_moderate.txt",
          "./hashes/hashes_strong.txt"]

output = ["./cracked_rulebased/cracked_weak.txt",
          "./cracked_rulebased/cracked_moderate.txt",
          "./cracked_rulebased/cracked_strong.txt"]

def main():
    for i in range(3):
        hashcat_command = [
            'hashcat',
            '-m', '0',
            '-a', '0',
            '-r', rule_file,
            '-o', output[i],
            hashes[i],
            wordlist
        ]
         
        process = subprocess.Popen(
            hashcat_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end='')
        
        process.wait()

        show_command = [
            'hashcat',
            '-m', '0',
            '--show',
            hashes[i]
        ]

        show_process = subprocess.Popen(
            show_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        cracked_hashes = ""

        for line in show_process.stdout:
            cracked_hashes += line

        with open(output[i], 'w') as f_out:
            f_out.write(cracked_hashes)

        show_process.wait()

if __name__ == "__main__":
    main()