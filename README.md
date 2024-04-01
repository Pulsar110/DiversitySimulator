# DiversitySimulator

### Modules

Dynamics
- Swap
    - RandomSwapper: Randomly select a pair of vertices and swap them if both of their utilities can.
    - UtilityOrderedSwapper: Iterate by priority based on the utility of the vertex.
- Swap conditions:
    - INDIVIDUAL_GREATER: swap if both new utilities are greater. 
    - INDIVIDUAL_NO_WORSE: swap if both new utilities are equal or greater and at least one is greater. 
    - SUM_GREATER: swap if the sum of both new utilities greater.
    - COLLECTIVE_GREATER: (not implemented) swap if the collective new utilities is greater.

Graph Environments
- Grid 
    - GridWord: Grid world that can be representated as an n-dimensional array (np.ndarray). With all vertices having the same degree.

Graph Initializations
- Grid Initialization
    - random_init: Random type assignment in the world.
    - block_init: Assign the types in blocks.
- Shelling initialization

Metrics
- social_welfare_metric: Sum of utilities of vertex in the graph environment. 
- diversity_metrics
    - degree_of_intergration: DOI_k, the percentage of vertices with at least k neighbouring vertices of a different type to itself.
    - percentage_of_segregated_verticies: Percentage of vertices in the graph with no neighbour of different type.
    - number_of_colorful_edges: The percentage of colorful edges, that is, connections between vertices of different type.
    - social_welfare: Sum of utilities compared with the best and worst case.

Utilities
- Neighborhood vector metrics
    - BinaryDiversityUtility: 1 if one of its neighbours is a different type than itself, 0 otherwise.
    - CountDiversityUtility: Count the number of neighbours with different type than itself.
    - TypeCountingDiversityUtility: Count the number of different types in the close neighborhood without counting its own type.
    - SchellingSegregationUtility: The fraction of its neighours that are the same type than itself. 
    - AntiSchellingSegregationUtility (not used): The fraction of its neighours that are not the same type than itself.
    - EntropyDivertiyUtility: The entropy of the neighbours type distribution.

### Experiments
- Setups
    - Worlds: CIRCLE_WORLD(40), CYLINDER_WORLD(2,40), GRID_4DEG_WORLD(20,20), GRID_8DEG_WORLD(20,20)
    - Initilialization: random_init, block_init, shelling initialization 
    - Swap: UtilityOrderedSwapper
    - Swap conditions: INDIVIDUAL_GREATER, INDIVIDUAL_NO_WORSE, SUM_GREATER
    - Utilities: BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountingDiversity, EntropyDivertiyUtility

- Metrics (diversity metrics)
    - social_welfare
    - degree_of_intergration
    - percentage_of_segregated_verticies
    - number_of_colorful_edges

- Number of runs: 10