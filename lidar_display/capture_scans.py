import os.path
import pickle

from lidar_display import lidarpy, lidar_reader

def main():
    lidar = lidarpy.Lidar("/dev/tty.usbserial-0001")
    if not lidar.connect():
        print('failed to connect')
        sys.exit(1)

    lidar.start_motor()

    reader = lidar_reader.LidarReader(lidar)

    output_dir = os.path.join(os.path.dirname(__file__), 'scans')

    for i in range(20):
        print(f'capture {i}')

        sc = reader.fetch_contour_from_lidar()

        with open(os.path.join(output_dir, f'scan_{i}.pickle'), 'wb') as f:
            pickle.dump(sc, f)

    print('done')

if __name__ == '__main__':
    main()
