# DiversitySimulator v2

### Modules
Dynamics
- Swap
    - RandomSwapper: Randomly select a pair of vertices and swap them if both of their utilities can.
    - UtilityOrderedSwapper: Iterate by priority based on the utility of the vertex. Small utility first. 
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
    - random_init: Random type assignment in the world. Choose the type from uniform distribution between 0 and `number_of_types`-1.
    - equitable_init: Randomly distribute equitable amount of types in the world. Randomly permute all indices of the vertices in the world, then assign type one after another such that we have the number of vertices for each type differ by at most 1.
- Shelling initialization after random or equitable initialzation, run the Schelling segregation algorithm. Swap according to SchellingSegregationUtility (no threshold).
	- shelling_random_init: Apply Schelling algorithm on top of random_init.
    - shelling_equitable_init: Apply Schelling algorithm on top of equitable_init.

Metrics
- social_welfare_metric: Sum of utilities of vertex in the graph environment. 
- diversity_metrics (all normalized between 0 and 1, the larger the better)
    - degree_of_intergration: DOI_k, the percentage of vertices with at least k neighbouring vertices of a different type to itself.
    - percentage_of_segregated_verticies: Percentage of vertices in the graph with no neighbour of different type.
    - number_of_colorful_edges: The percentage of colorful edges, that is, connections between vertices of different type. It is normalized by the best case (total number of edges). 
    - social_welfare: Sum of utilities compared with the best and worst case.
    - l2: Inverse of the sum of eveness of the open neighbourhood multiplied by the best case. 
    - closed_l2: l2 but computed with the closed neighbourhood.

Utilities
- Neighborhood vector metrics
    - BinaryDiversityUtility: 1 if one of its neighbours is a different type than itself, 0 otherwise.
    - DifferenceCountDiversityUtility: Count the number of neighbours with different type than itself.
    - TypeCountingDiversityUtility: Count the number of different types in the close neighborhood without counting its own type.
    - SchellingSegregationUtility: The fraction of its neighours that are the same type than itself. If there is a threshold, then it is a binary value indicating whether the fraction is larger than the threshold.
    - AntiSchellingSegregationUtility (not used): The fraction of its neighours that are not the same type than itself.
    - EntropyDivertiyUtility: The entropy of the neighbours type distribution.

### Experiments
- Setups
    - Worlds: CIRCLE_WORLD, CYLINDER_WORLD, GRID_4DEG_WORLD, GRID_8DEG_WORLD
    - World size: 400, 900
    - Types: 2-9
    - Initilialization: random_init, equitable_init, schelling_random_init, schelling_equitable_init
    - Swap: UtilityOrderedSwapper
    - Swap conditions: INDIVIDUAL_GREATER
    - Utilities: BinaryDiversityUtility, TypeCountingDiversityUtility, DifferenceCountDiversityUtility

- Metrics (diversity metrics)
    - social_welfare
    - degree_of_intergration
    - percentage_of_segregated_verticies
    - number_of_colorful_edges
    - l2

- Number of runs: 30, 50

### Results
Result are in the `results_<time>` directories. 

- results_may_2024: with EntropyDivertiyUtility, random initialization, without l2 metric
- results_oct_2024: without EntropyDivertiyUtility, with random and equitable initialization, with l2 metric