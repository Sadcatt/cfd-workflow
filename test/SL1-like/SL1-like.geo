SetFactory("OpenCASCADE");

// Parameters for outer and inner cylinders
R_outer = 1.0;
R_inner = 0.3;
H = 2.0;
lc = 0.1;

// Outer cylinder domain
Cylinder(1, 0, 0, 0, 0, 0, H, R_outer);

// Inner cylinder to subtract from the outer domain
Cylinder(2, 0, 0, 0, 0, 0, H, R_inner);

// Boolean subtraction: outer cylinder minus inner cylinder
domain[] = BooleanDifference{ Volume{1}; Delete; }{ Volume{2}; Delete; };

// Define a physical volume for the CFD fluid domain
Physical Volume("FluidDomain") = {domain[0]};

// Mesh size control
Mesh.CharacteristicLengthMax = lc;
Mesh.CharacteristicLengthMin = lc;
