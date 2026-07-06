"""A* path planner on a 2D grid."""

import numpy as np
from heapq import heappush, heappop


class AStarPlanner:
    """A* planner on an occupancy grid.

    Args:
        resolution: Grid cell size (m).
        obstacle_threshold: Value above which a cell is an obstacle.
    """

    def __init__(self, resolution: float = 0.1, obstacle_threshold: int = 128):
        self.resolution = resolution
        self.obstacle_threshold = obstacle_threshold

    def plan(
        self, grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[float, float]]:
        """Find a path from start to goal.

        Args:
            grid: 2D array (H, W). Higher values = obstacles.
            start: (row, col) start cell.
            goal: (row, col) goal cell.

        Returns:
            List of (x, y) waypoints in world coordinates, or empty if no path.
        """
        h, w = grid.shape
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        neighbors = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),
        ]

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return self._reconstruct(came_from, current, self.resolution)

            for dr, dc in neighbors:
                nr, nc = current[0] + dr, current[1] + dc
                if 0 <= nr < h and 0 <= nc < w:
                    if grid[nr, nc] >= self.obstacle_threshold:
                        continue

                    # diagonal cost is sqrt(2)
                    move_cost = np.sqrt(dr ** 2 + dc ** 2)
                    tentative_g = g_score[current] + move_cost

                    neighbor = (nr, nc)
                    if tentative_g < g_score.get(neighbor, float("inf")):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f = tentative_g + self._heuristic(neighbor, goal)
                        heappush(open_set, (f, neighbor))

        return []  # no path found

    def _heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        """Octile distance heuristic."""
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        return max(dr, dc) + (np.sqrt(2) - 1) * min(dr, dc)

    def _reconstruct(
        self, came_from: dict, current: tuple[int, int], res: float
    ) -> list[tuple[float, float]]:
        """Reconstruct path and convert to world coordinates."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()

        # convert to world coords (center of cell)
        return [(c * res + res / 2, r * res + res / 2) for r, c in path]


def demo():
    """Sanity check: simple 10x10 grid with a path."""
    planner = AStarPlanner(resolution=1.0)
    grid = np.zeros((10, 10), dtype=int)
    grid[3, 3:7] = 128  # wall

    path = planner.plan(grid, (0, 0), (9, 9))
    assert len(path) > 0, "should find a path"
    assert path[0][0] < path[-1][0], "should go from left to right"
    print("a_star: all checks passed")


if __name__ == "__main__":
    demo()
