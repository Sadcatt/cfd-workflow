// D-shape domain with infinite 2d cylinder in the centre

domainHeight = 4; //meters
domainLength = 10; //meters
inletRadius = domainHeight/2; //meters

mesh_number = 0.05;

cylinderRadius = 0.1; //meters

// Circle points 
Point(1) = {0, 0, 0, mesh_number};
Point(2) = {-cylinderRadius/2, 0, 0, mesh_number};
Point(3) = {cylinderRadius/2, 0, 0, mesh_number};

// Domain border points
Point(4) = {-domainLength/2, domainHeight/2, 0, mesh_number}; //top left
Point(5) = {domainLength/2, domainHeight/2, 0, mesh_number}; //top right
Point(6) = {domainLength/2, -domainHeight/2, 0, mesh_number}; //bottom right
Point(7) = {-domainLength/2, -domainHeight/2, 0, mesh_number}; //bottom left


// Circle arcs
Circle(1) = {2, 1, 3}; //top half of circle
Circle(2) = {3, 1, 2}; //bottom half of circle

// Domain border lines
Line(3) = {4, 5}; //top
Line(4) = {5, 6}; //right
Line(5) = {6, 7}; //bottom
Line(6) = {7, 4}; //left

// Closed contours
Curve Loop(1) = {1, 2}; //circle
Curve Loop(2) = {3, 4, 5, 6}; //domain border

// Surface from contours
Plane Surface(1) = {1, 2}; //either order works for this case, however tutorial said to use the domain before the circle as they were working the other way round

// Transfinite Curve at cylinder test
Transfinite Curve {2, 1} = 200 Using Progression 1;
//Transfinite Surface {1};
// Physical Grouping (Named selections)
//Physical Line("Inlet") = {6};
//Physical Line("Outlet") = {4};
//Physical Line("Domain Wall") = {5, 7};
Physical Line ("Farfield") = {3, 4, 5, 6};
Physical Line ("Cylinder Wall") = {1, 2};

Physical Surface("Interior Fluid") = {1};

// Mesh the domain
Mesh 2;

// Mesh visibility options
Mesh.SurfaceFaces = 1;
//Mesh.Points = 1;

// Save generated mesh to directory
Save "cyl.msh";
Save "cyl.su2";

