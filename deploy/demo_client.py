"""Client-end for the ASR demo."""

if __name__ == "__main__":

    from pynput import keyboard
    import datetime as dt
    import struct
    import socket
    import sys
    import argparse
    import pyaudio

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host_ip",
        default="localhost",
        type=str,
        help="Server IP address. (default: %(default)s)")
    parser.add_argument(
        "--host_port",
        default=8086,
        type=int,
        help="Server Port. (default: %(default)s)")
    args = parser.parse_args()

    is_recording = False
    enable_trigger_record = True


    def on_press(key):
        """On-press keyboard callback function."""
        global is_recording, enable_trigger_record
        if key == keyboard.Key.space:
            if (not is_recording) and enable_trigger_record:
                sys.stdout.write("Start Recording ... ")
                sys.stdout.flush()
                is_recording = True


    def on_release(key):
        """On-release keyboard callback function."""
        global is_recording, enable_trigger_record
        if key == keyboard.Key.esc:
            return False
        elif key == keyboard.Key.space:
            if is_recording == True:
                is_recording = False


    data_list = []

    def callback(in_data, frame_count, time_info, status):
        """Audio recorder's stream callback function."""
        global data_list, is_recording, enable_trigger_record
        if is_recording:
            data_list.append(in_data)
            enable_trigger_record = False
        elif len(data_list) > 0:
            # Connect to server and send data
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((args.host_ip, args.host_port))
            sent = ''.join(data_list)
            start = dt.datetime.now()
            sock.sendall(struct.pack('>i', len(sent)) + sent)
            print('Speech[length=%d] Sent.' % len(sent))
            # Receive data from the server and shut down
            received = sock.recv(1024)
            print('Time: {0}'.format(dt.datetime.now() - start))
            print("Recognition Results: {}".format(received))
            sock.close()
            data_list = []
        enable_trigger_record = True
        return (in_data, pyaudio.paContinue)

    # prepare audio recorder
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt32,
        channels=1,
        rate=8000,
        input=True,
        stream_callback=callback)
    stream.start_stream()
    print("Stream started ...")

    import time
    import threading
    def only_sleep(n):
        global is_recording, enable_trigger_record
        is_recording = True
        time.sleep(n)
        is_recording = False
        time.sleep(0.1)
    ts = threading.Thread(target=only_sleep, args=(5,))
    ts.start()
    ts.join()

    # close up
    stream.stop_stream()
    stream.close()
    p.terminate()
