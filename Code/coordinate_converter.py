import math
import argparse


def calculate_relative_vector(player, boss):
    # Unpack positions and angles (angle is not used in the vector calculation)
    player_x, player_y, player_z, player_angle = player
    boss_x, boss_y, boss_z, boss_angle = boss

    # Compute displacement vector components
    dx = boss_x - player_x
    dy = boss_y - player_y
    dz = boss_z - player_z

    # Euclidean distance between player and boss
    distance = math.sqrt(dx**2 + dy**2 + dz**2)

    # Compute the horizontal angle (in degrees) that the player must face
    # using the x and z components; adjust as needed if your coordinate system differs.
    target_angle = math.degrees(math.atan2(dz, dx))

    return (dx, dy, dz), distance, target_angle


def main():
    parser = argparse.ArgumentParser(
        description="Convert player and boss coordinates into a relative vector."
    )
    parser.add_argument(
        "--player", nargs=4, type=float, required=True,
        help="Player x y z angle"
    )
    parser.add_argument(
        "--boss", nargs=4, type=float, required=True,
        help="Boss x y z angle"
    )
    args = parser.parse_args()

    player = args.player
    boss = args.boss

    relative_vector, distance, target_angle = calculate_relative_vector(
        player, boss)

    print("Relative vector (from player to boss):", relative_vector)
    print("Distance between player and boss:", distance)
    print("Player should face angle (degrees):", target_angle)


if __name__ == '__main__':
    main()
