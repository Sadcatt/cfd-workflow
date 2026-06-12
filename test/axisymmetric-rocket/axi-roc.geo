//// Variables Area
rocketLengthTot = 1;    //m
bodyRadius = 0.1;       //m
boattailRadius = 0.06;  //m
noseLength = 0.3;       //m
bodyLength = 0.6;       //m
boattailLength = 0.1;   //m

domainRadius = 10;
domainDownstream = 20;

boundaryMeshSize = 0.05;
farfieldMeshSize = 0.1;

//// Geometry Area

// Rocket Body
Point(1) = {0, 0, 0, boundaryMeshSize}; //nosecone tip
Point(2) = {noseLength, bodyRadius, 0, boundaryMeshSize}; //nosecone-body transition
Point(3) = {noseLength+bodyLength, bodyRadius, 0, boundaryMeshSize}; //body-boattail transition
Point(4) = {noseLength+bodyLength+boattailLength, boattailRadius, boundaryMeshSize}; //end of boattail
Point(5) = {noseLength+bodyLength+boattailLength, 0, 0, boundaryMeshSize};

Line(1) = {1,2}; //nosecone
Line(2) = {2,3}; //body
Line(3) = {3,4}; //boattail
Line(4) = {4,5}; //exhaust


// Domain Definition
// domain designed to be half-D-shaped axisymmetric
Point(6) = {-domainRadius, 0, 0, farfieldMeshSize};
Point(7) = {0, domainRadius, 0, 0, farfieldMeshSize};
Point(8) = {domainDownstream, domainRadius, 0, farfieldMeshSize};
Point(9) = {domainDownstream, 0, 0, farfieldMeshSize};
Point(10) = {noseLength+bodyLength+boattailLength, domainRadius, 0, farfieldMeshSize};
Point(11) = {domainDownstream, boattailRadius, 0, farfieldMeshSize};

Circle(5) = {6,1,7}; //using nosecone tip as centre point
Line(6) = {7,10};
Line(7) = {8,11};

// Connecting domain to rocket
Line(8) = {6,1};
Line(9) = {5,9};


// Splitting domain into areas for transfinite operations
Line(10) = {1,7};


Line(11) = {4,10};


Line(12) = {4,11};
Line(13) = {10,8};
Line(14) = {11,9};


// For single section domain: Closing whole domain into curve loop
//Curve Loop(1) = {5, 6, 7, -9, -4, -3, -2, -1, -8};
//Plane Surface(1) = {1};


// For multi-domain

Curve Loop(1) = {10, -5, 8};
Curve Loop(2) = {6, -11, -3, -2, -1, 10};
Curve Loop(3) = {13, 7, -12, 11};
Curve Loop(4) = {12, 14, -9, -4};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};

// assigning transfinites

Transfinite Line {10,11} = 10 Using Progression 1;

Transfinite Surface {2};