WATER = "0"
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        visited = set()
        cells_to_visit = []

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                num_islands += 1
                visited.add((row, col))
                cells_to_visit.append((row, col))

                while cells_to_visit:
                    cur_row, cur_col = cells_to_visit.pop()
                    for d_row, d_col in DIRECTIONS:
                        next_row = cur_row + d_row
                        next_col = cur_col + d_col

                        if not (0 <= next_row < num_rows and 0 <= next_col < num_cols):
                            continue
                        if grid[next_row][next_col] == WATER:
                            continue
                        if (next_row, next_col) in visited:
                            continue

                        visited.add((next_row, next_col))
                        cells_to_visit.append((next_row, next_col))

        return num_islands
