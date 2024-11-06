import subprocess
import os

wordlist = "./rockyou.txt"
rule_file = "./rules/rockyou-30000.rule"
rule_file_2 = "./rules/best64.rule"

hashes = [
    "./hashes/hashes_weak.txt",
    "./hashes/hashes_moderate.txt",
    "./hashes/hashes_strong.txt"
]

output = [
    "./cracked_rulebased/cracked_weak.txt",
    "./cracked_rulebased/cracked_moderate.txt",
    "./cracked_rulebased/cracked_strong.txt"
]

def read_hashes(hash_file):
    with open(hash_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    for i in range(len(hashes)):
        current_hash_file = hashes[i]
        current_output_file = output[i]

        all_hashes = read_hashes(current_hash_file)

        hashcat_command = [
            'hashcat',
            '-m', '0',
            '-a', '0',
            '-r', rule_file,
            '-o', 'temp_cracked.txt',
            current_hash_file,
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
            current_hash_file
        ]

        show_process = subprocess.Popen(
            show_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        cracked_output = show_process.communicate()[0]

        cracked_hash_to_password = {}
        for line in cracked_output.strip().split('\n'):
            if ':' in line:
                hash_part, password = line.split(':', 1)
                cracked_hash_to_password[hash_part] = password

        password_list = [
            cracked_hash_to_password.get(hash_value, '')
            for hash_value in all_hashes
        ]

        with open(current_output_file, 'w') as f_out:
            f_out.write(str(password_list))

        if os.path.exists('temp_cracked.txt'):
            os.remove('temp_cracked.txt')

if __name__ == "__main__":
    main()