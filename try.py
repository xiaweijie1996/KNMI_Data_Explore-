import traceback
import sys
 
from eccodes import *
 
file_path = r'HARM43_V1_P1_2024121611\HA43_N20_202412161100_03900_GB'
VERBOSE = 1  # verbose error reporting

# Open the GRIB file
with open(file_path, 'rb') as f:
    print("Debugging GRIB file: Listing all keys and their values...\n")
    message_count = 0

    while True:
        try:
            # Load the next GRIB message
            gid = codes_grib_new_from_file(f)
            if gid is None:  # End of file
                break

            message_count += 1
            print(f"\n--- GRIB Message {message_count} ---")

            # Check if the message has any keys
            iterator = codes_keys_iterator_new(gid, 'all')
            keys_found = False

            # Iterate over all keys
            while codes_keys_iterator_next(iterator):
                keys_found = True
                key = codes_keys_iterator_get_name(iterator)
                try:
                    value = codes_get(gid, key)
                    print(f"{key}: {value}")
                except CodesInternalError:
                    # Ignore keys that cannot be retrieved
                    continue

            if not keys_found:
                print("No keys found in this message. Check file structure or configuration.")

            # Release resources for this message
            codes_keys_iterator_delete(iterator)
            codes_release(gid)

        except CodesInternalError as e:
            print(f"Error reading GRIB file: {e}")
            break

    if message_count == 0:
        print("No GRIB messages found in the file. Ensure the file is valid.")

    print("\nFinished debugging the GRIB file.")