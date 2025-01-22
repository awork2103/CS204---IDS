import subprocess
import time
import asyncio

async def run_tshark():
    print("Running TShark instance")
    try:
        process = await asyncio.create_subprocess_exec(
            "/bin/bash", 
            "./runTShark.sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout, stderr
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

async def run_snort(): 
    print("Running Snort instance")
    try:
        process = await asyncio.create_subprocess_exec(
            "/bin/bash", 
            "./runSnort.sh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout, stderr
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

async def main():
    # CONSTANTS
    TSHARK_INTERVAL = 60  # 60 seconds
    running_tasks = set()

    # Every half of TSHARK_INTERVAL, run another Instance of TShark
    while True:
        # Create new task
        task = asyncio.create_task(run_tshark(), name="tshark")
        task2 = asyncio.create_task(run_snort(), name="snort")
        running_tasks.add(task)
        running_tasks.add(task2)
        
        # Clean up completed tasks
        done_tasks = {t for t in running_tasks if t.done()}
        for t in done_tasks:
            running_tasks.remove(t)
            try:
                stdout, stderr = await t
                print(f"Task {t.get_name()} completed with result: {stdout}")
            except Exception as e:
                print(f"Task {t.get_name()} failed: {e}")
        
        print(f"Current running tasks: {len(running_tasks)}")
        await asyncio.sleep(TSHARK_INTERVAL/2)

def setup_folders():
    subprocess.run(["rm", "-rf", "./output"])
    subprocess.run(["rm", "-rf", "./csv"])
    subprocess.run(["rm", "-rf", "./virustotal-files"])
    subprocess.run(["rm", "-rf", "./snortlog"])

    subprocess.run(["mkdir", "./output"])
    subprocess.run(["mkdir", "./csv"])
    subprocess.run(["mkdir", "./virustotal-files"])
    subprocess.run(["mkdir", "./snortlog"])

if __name__ == "__main__":
    setup_folders()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
