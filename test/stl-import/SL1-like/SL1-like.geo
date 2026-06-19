//// Welcome to the test of 3d meshing using the SL1 Skinny that I made from publically available data and is therefore not in violation of any agreements I ay be subject to now or in the future.
// Varaibles
// Creation of Domain areas for the sim
// STL Preperation
// Process the mesh and add things like transfinite and sizings
// Unify the areas, recombine, etc
// Add physical groups
// Save and export

SetFactory ("OpenCASCADE");

// ------------- Variables --------------
lc = 2000;
domainRadius = 5000; //m
domainLength = 40000; //m

bluntingLength = 67.04; //mm
noseconeLength = 3300;
pretransitionLength = 16500;
transitionLength = 5500;
posttrantionLength = 4400;
nozzleLength = 300;

// -------------- Domain ----------------
// creating cylindrical domain with 2D rectangular domain
Point(1) = {0, 1000, 0, lc};
Point(2) = {0, -domainLength, 0, lc};
Point(3) = {0, -domainLength, domainRadius, lc};
Point(4) = {0, 1000, domainRadius, lc};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

Extrude {{0, 1, 0}, {0, 0, 0}, Pi/4} {Surface{1};}
//Delete {Surface{1}};
//Coherence;


// ------------- STL Prep. --------------
v() = ShapeFromFile( "SL1-Skinny.STEP");
//HealShapes;
//Coherence;
//Coherence;
//Transfinite Surface{73, 81} //20 Using Progression 1;
//+
BooleanDifference{ Volume{1}; Delete;}{ Volume{2}; Volume{3}; Volume{4}; Volume{5}; Volume{6}; Volume{7}; Volume{8}; Volume{9}; Volume{10}; Delete;}
//Coherence;
//BooleanDifference{ Volume{3}; }{ Volume{2}; Delete; }
//Delete {Surface{1}; Surface{5};}
//Mesh 3;
//noseconeBluntingCoords[] = Point{16};

//Transfinite Line {58, 60} = 60 Using Progression 1;
//Transfinite Line {51, 52, 59, 68} = 30 Using Progression 1;
////Trasnfinite Line {} = 30 Using Progression 1;
//Transfinite Line {57, 67, 65, 63, 64, 66} = 60 Using Progression 1;
//
//Transfinite Line {61, 62} = 40 Using Progression 1;//NOSECONE LENGTH
//
////Transfinite Surface {34, 38};
//
//Transfinite Surface {36, 37};
//
//Transfinite Surface {35, 39};
//
//Recombine Surface "*"; // this is what turns the triangles into a quad structured mesh!//+
//Field[1] = BoundaryLayer;
////+
//Field[1].CurvesList = {16};
////+
//Delete Field [1];
//Mesh.MeshSizeFromCurvature = 200;
//Mesh.MeshSizeFromPoints = 10;

// contrain min/max mesh size
Mesh.MeshSizeFromCurvature = 2000;
Mesh.MeshSizeFromPoints = 1;
Mesh.MeshSizeMin = 10;
Mesh.MeshSizeMax = 1000;
