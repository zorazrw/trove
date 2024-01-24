"""Program Execution Utilities."""

import subprocess


def execute_code_wrapped(
    code_pieces: list[str], 
    exec_file: str = "tmp_exec.py", 
    timeout: int = 100,
) -> tuple[bool, str]:
    try:
        # write all code pieces into a file
        with open(exec_file, 'w') as fw:
            fw.write('\n\n'.join(code_pieces))

        # execute code file
        result = subprocess.run(
            ['python', exec_file], 
            capture_output=True, 
            check=False, text=True,
            timeout=timeout,
        )
        if result.returncode != 0:  # execution failed
            error_msgs = result.stderr.strip().split("\n")
            new_msgs, want_next = [], False 
            for em in error_msgs:
                if "Trackback" in em:
                    new_msgs.append(em)
                elif em == error_msgs[-1]:
                    new_msgs.append(em)
                elif exec_file in em:
                    s = em.index('"/') + 1
                    e = em.index(f'/{exec_file}') + 1
                    new_msgs.append(em.replace(em[s:e], ""))
                    want_next = True 
                elif want_next:
                    new_msgs.append(em)
                    want_next = False
            error_msg = "\n".join(new_msgs).strip()
            return False, error_msg
        else:  # execution success
            output = result.stdout.strip()
            return True, output
    except subprocess.TimeoutExpired:
        return False, "Timeout detected in running subprocess"
    except Exception as e:
        return False, f"Unknown error in running subprocess ({e})"
