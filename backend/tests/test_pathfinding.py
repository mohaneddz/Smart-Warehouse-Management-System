from backend.core.pathfinding import PathfindingSimulation

def test_pathfinding():
    # Create a 10x10 grid
    sim = PathfindingSimulation((10, 10))
    
    # Set start and goal positions
    sim.set_start((0, 0))
    sim.set_goal((9, 9))
    
    # Add some obstacles
    sim.add_obstacle((2, 2))
    sim.add_obstacle((2, 3))
    sim.add_obstacle((3, 2))
    sim.add_obstacle((4, 4))
    sim.add_obstacle((5, 5))
    sim.add_obstacle((6, 6))
    
    # Find the path
    path = sim.find_path()
    
    if path:
        print("Path found!")
        print("Path length:", len(path))
        print("Path:", path)
        
        # Visualize the path
        for y in range(10):
            for x in range(10):
                pos = (x, y)
                if pos == sim.start:
                    print("S", end=" ")
                elif pos == sim.goal:
                    print("G", end=" ")
                elif pos in sim.obstacles:
                    print("X", end=" ")
                elif pos in path:
                    print("*", end=" ")
                else:
                    print(".", end=" ")
            print()
    else:
        print("No path found!")

if __name__ == "__main__":
    test_pathfinding() 