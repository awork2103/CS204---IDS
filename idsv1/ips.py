# import subprocess
# import time
# import asyncio

# # TODO RUN TSHARK
# # async def runTShark():
# #     # Run TShark 
# #     # TShark will capture traffic then output to pcap file
# #     # Once TShark has finished outputing file --> move to the working folder for VT, RF Model, Snort
# #     print("Running TShark")
# #     await asyncio.create_subprocess_exec(["/bin/bash", "./runTShark.sh"])
# #     # await asyncio.create_subprocess_exec(
# #     #     "/bin/bash", "./runTShark.sh",
# #     #     stdout=asyncio.subprocess.PIPE,
# #     #     stderr=asyncio.subprocess.PIPE
# #     # )
# #     print("Completed Running TShark")

# async def run_tshark():
#     try:
#         process = await asyncio.create_subprocess_exec(
#             "/bin/bash", 
#             "./runTShark.sh",
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         stdout, stderr = await process.communicate()
#         return stdout, stderr
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise

# async def main():
#     # CONSTANTS
#     TSHARK_INTERVAL = 60;   # 60 seconds

#     # Every half of TSHARK_INTERVAL, run another Instance of TShark
#     while(True) :
#         task = asyncio.create_task(run_tshark())
#         try:
#             result = await task
#             # Handle the result
#             print(f"Task result: {result}")
#         except Exception as e:
#             print(f"Task failed: {e}")
#         # asyncio.create_task(runTShark())
#         await asyncio.sleep(TSHARK_INTERVAL/2)

# def setup_folders():
#     subprocess.run(["rm", "-rf", "./output"])
#     subprocess.run(["rm", "-rf", "./csv"])
#     subprocess.run(["rm", "-rf", "./virustotal-files"])
#     subprocess.run(["rm", "-rf", "./snortlog"])

#     subprocess.run(["mkdir", "./output"])
#     subprocess.run(["mkdir", "./csv"])
#     subprocess.run(["mkdir", "./virustotal-files"])
#     subprocess.run(["mkdir", "./snortlog"])

    
# if __name__ == "__main__":
#     setup_folders()
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\nShutting down...")


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

async def main():
    # CONSTANTS
    TSHARK_INTERVAL = 60  # 60 seconds
    running_tasks = set()

    # Every half of TSHARK_INTERVAL, run another Instance of TShark
    while True:
        # Create new task
        task = asyncio.create_task(run_tshark())
        running_tasks.add(task)
        
        # Clean up completed tasks
        done_tasks = {t for t in running_tasks if t.done()}
        for t in done_tasks:
            running_tasks.remove(t)
            try:
                result = await t
                print(f"Task completed with result: {result}")
            except Exception as e:
                print(f"Task failed: {e}")
        
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
