import utime
def get_time():
    # Get the current timestamp in seconds since the epoch
    timestamp_s = utime.time()
    # Get the current timestamp in microseconds since the epoch
    timestamp_ns = utime.time_ns()

    # Convert the timestamp to a tuple of time values
    time_tuple = utime.localtime(int(timestamp_s))
    millis =  (timestamp_ns - timestamp_s * 1000000000)
    # Format the time values into the desired format
    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:06d}".format(
        time_tuple[0],  # Year
        time_tuple[1],  # Month
        time_tuple[2],  # Day
        time_tuple[3],  # Hour
        time_tuple[4],  # Minute
        time_tuple[5],  # Second
        int(millis/1000)  # Microseconds
    )
    return formatted_time
