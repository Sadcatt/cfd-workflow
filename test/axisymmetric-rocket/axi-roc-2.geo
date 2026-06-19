//// Variables Area
//rocketLengthTot = 1;    //m
bodyRadius = 0.03;       //m
boattailRadius = 0.014;  //m
noseLength = 0.3;       //m
bodyLength = 1.0;       //m
boattailLength = 0.4;   //m

domainRadius = 30;
domainDownstream = 20;

boundaryMeshSize = 0.05;
farfieldMeshSize = 0.1;

// Domain Gen

Point(1)  = {0,                                     0,                  0};
Point(2)  = {noseLength,                            bodyRadius,         0};
Point(3)  = {noseLength+bodyLength,                 bodyRadius,         0};
Point(4)  = {noseLength+bodyLength+boattailLength,  boattailRadius,     0};
Point(5)  = {noseLength+bodyLength+boattailLength,  0,                  0};
Point(6)  = {domainDownstream,                      0,                  0};
Point(7)  = {domainDownstream,                      boattailRadius,     0};
Point(8)  = {domainDownstream,                      domainRadius,       0};
Point(9)  = {noseLength+bodyLength+boattailLength,  domainRadius,       0};
Point(10) = {noseLength+bodyLength,                 domainRadius,       0};
Point(11) = {noseLength,                            domainRadius,       0};
Point(12) = {0,                                     domainRadius,       0};
Point(13) = {-domainRadius,                         0,                  0};

Line(1)     = {1,   2};
Line(2)     = {2,   3};
Line(3)     = {3,   4};
Line(4)     = {4,   5};
Line(5)     = {5,   6};
Line(6)     = {6,   7};
Line(7)     = {7,   8};
Line(8)     = {8,   9};
Line(9)     = {9,   10};
Line(10)    = {10,  11};
Line(11)    = {11,  12};
Circle(12)  = {12,1,13};
Line(13)    = {13,  1};
Line(14)    = {1,   12};
Line(15)    = {2,   11};
Line(16)    = {3,   10};
Line(17)    = {4,   9};
Line(18)    = {4,   7};

// Assigning Surfaces

Curve Loop(1) = {14,    12,     13};
Curve Loop(2) = {1,     15,     11,     -14};
Curve Loop(3) = {2,     16,     10,     -15};
Curve Loop(4) = {3,     17,     9,      -16};
Curve Loop(5) = {18,    7,      8,      -17};
Curve Loop(6) = {4,     5,      6,      -18};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

// Transfinite

//vars
noseconeElements    = 10;
bodyElements        = 20;
boattailElements    = 8;
exhaustwakeElements = 8;
downstreamElements  = 20;
dinletElements      = 10;
verticalElements    = 60;

//settings
Transfinite Line {1,  11}                   = noseconeElements      Using Progression 1;
Transfinite Line {2,  10}                   = bodyElements          Using Progression 1;
Transfinite Line {3,  9}                    = boattailElements      Using Progression 1;
Transfinite Line {4,  6}                    = exhaustwakeElements   Using Progression 1;

Transfinite Line {5,  18, -8}               = downstreamElements    Using Progression 1.5;
Transfinite Line {12}                       = dinletElements        Using Progression 1;
Transfinite Line {-13, 14, 15, 16, 17, 7}   = verticalElements      Using Progression 1.3;

Transfinite Surface {1};
Transfinite Surface {2};
Transfinite Surface {3};
Transfinite Surface {4};
Transfinite Surface {5};
Transfinite Surface {6};

Coherence;
Recombine Surface "*"; // this is what turns the triangles into a quad structured mesh!
Mesh 2;

// Assignging Surfaces for SU2
// everything around the rocket is a farfield boundary
// the rocket is an euler boundary
// symmetry is a symmetry axisymmetric symmetry boundary
Physical Line ("Farfield") = {6, 7, 8, 9, 10, 11, 12, 12};
Physical Line ("Wall") = {1, 2, 3, 4, 5};
Physical Line ("Symmetry") = {13, 5};

Physical Surface ("Interior Fluid") = {1, 2, 3, 4, 5, 6};

Save "axi-roc-2.su2";