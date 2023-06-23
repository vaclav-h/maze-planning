import sys
import argparse
from ff_maze import FFMaze
from vi_maze import VIMaze
from utils import visualize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    parser.add_argument('-m', '--method', type=str, choices=['ff', 'vi'], required=True)
    args = parser.parse_args()
    traverse_maze(args)


def traverse_maze(args):
    if args.method == 'ff':
        maze = FFMaze(args.file)
        reward, plan = maze.traverse((1, 1))
    elif args.method == 'vi':
        maze = VIMaze(args.file)
        maze.value_iteration(discount=0.99999, eps=1e-8, max_iter=2000)
        reward, plan = maze.traverse((1, 1))
    print(f"Reward: {reward}")
    visualize(maze.maze, plan)


if __name__ == '__main__':
    main()
