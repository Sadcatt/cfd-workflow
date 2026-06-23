## this entire thing is hallucinated by copilot, i dont know if it works lol
# was meant to take all the body part objects and contain them together for computation or plotting

from dataclasses import dataclass
from math import pi
from typing import Any, Iterable, List, Tuple


@dataclass
class fuselage:
    """Represent a rocket fuselage by combining nosecone and body contour objects."""

    noseCone: Any
    bodyContour: Any

    def __post_init__(self) -> None:
        """Validate that interfacing component sizes match at initialization."""
        self._validate_interface()

    def _get_part_points(self, part: Any) -> List[Tuple[float, float]]:
        """Retrieve and normalize contour points from a part object."""
        points = getattr(part, "coordinates", None)
        if callable(points):
            points = points()
        if points is None:
            return []
        return self._flatten_points(points)

    def _validate_interface(self) -> None:
        """Ensure the nosecone and body contour meet at a common interface radius."""
        nose_points = self._get_part_points(self.noseCone)
        body_points = self._get_part_points(self.bodyContour)
        if not nose_points or not body_points:
            raise ValueError(
                "noseCone and bodyContour must provide valid contour points"
            )

        nose_end_radius = abs(nose_points[-1][1])
        body_start_radius = abs(body_points[0][1])
        if abs(nose_end_radius - body_start_radius) > 1e-6:
            raise ValueError(
                "noseCone end radius and bodyContour start radius must match "
                "at the interface; validate input component sizes."
            )

    def _adjust_interfacing_radii(
        self,
        nose_points: List[Tuple[float, float]],
        body_points: List[Tuple[float, float]],
    ) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        """Scale interfacing components so their shared radius remains consistent."""
        if not nose_points or not body_points:
            return nose_points, body_points

        nose_end_radius = abs(nose_points[-1][1])
        body_start_radius = abs(body_points[0][1])
        if abs(nose_end_radius - body_start_radius) <= 1e-6:
            return nose_points, body_points

        target_radius = (nose_end_radius + body_start_radius) / 2.0
        if nose_end_radius > 0:
            nose_scale = target_radius / nose_end_radius
            nose_points = [(x, y * nose_scale) for x, y in nose_points]
        if body_start_radius > 0:
            body_scale = target_radius / body_start_radius
            body_points = [(x, y * body_scale) for x, y in body_points]

        return nose_points, body_points

    def combined_contour(self) -> List[Tuple[float, float]]:
        """Return a combined list of contour points from the nosecone and body contour."""
        # Step 1: read the coordinate source from each attached part
        nosePoints = getattr(self.noseCone, "coordinates", None)
        bodyPoints = getattr(self.bodyContour, "coordinates", None)

        # Step 2: if the coordinate sources are callables, invoke them to retrieve data
        if callable(nosePoints):
            nosePoints = nosePoints()
        if callable(bodyPoints):
            bodyPoints = bodyPoints()

        # Step 3: validate each part supplied contour data
        if nosePoints is None or bodyPoints is None:
            raise ValueError(
                "noseCone and bodyContour must provide a 'coordinates' attribute or method"
            )

        # Step 4: normalize each contour, align interface radii, and concatenate
        normalizedNosePoints = self._flatten_points(nosePoints)
        normalizedBodyPoints = self._flatten_points(bodyPoints)
        normalizedNosePoints, normalizedBodyPoints = self._adjust_interfacing_radii(
            normalizedNosePoints, normalizedBodyPoints
        )
        return normalizedNosePoints + normalizedBodyPoints

    def _flatten_points(self, points: Any) -> List[Tuple[float, float]]:
        """Normalize contour points into a list of (x, y) tuples."""
        # Step 1: if a dict is supplied, retrieve the embedded points list
        if isinstance(points, dict):
            points = points.get("points", [])

        # Step 2: ensure each point is returned as a tuple
        return [tuple(point) for point in points]

    def total_length(self) -> float:
        """Return the fuselage length using the combined contour points."""
        # Step 1: collect the full combined contour
        contour = self.combined_contour()
        if not contour:
            return 0.0

        # Step 2: extract x coordinates from all contour points
        xs = [point[0] for point in contour]

        # Step 3: compute the length as the x-range of the contour
        return max(xs) - min(xs)

    def max_radius(self) -> float:
        """Return the maximum radius from the combined contour points."""
        # Step 1: build the combined contour
        contour = self.combined_contour()
        if not contour:
            return 0.0

        # Step 2: compute the maximum absolute y coordinate
        ys = [abs(point[1]) for point in contour]
        return max(ys)

    def reference_cross_sectional_area(self) -> float:
        """Return a reference cross sectional area using the largest body radius."""
        # Step 1: determine the maximum radius from the contour
        radius = self.max_radius()

        # Step 2: compute the reference cross-sectional area
        return pi * radius ** 2

    def drag_force(
        self,
        dragCoefficient: float,
        velocity: float = None,
        airDensity: float = 1.225,
        dynamicPressure: float = None,
    ) -> float:
        """Calculate drag force from a drag coefficient and flow conditions."""
        # Step 1: determine dynamic pressure from either direct input or velocity
        if dynamicPressure is None:
            if velocity is None:
                raise ValueError(
                    "Either velocity or dynamicPressure must be provided"
                )
            dynamicPressure = 0.5 * airDensity * velocity * velocity

        # Step 2: compute drag force using the current reference area
        referenceArea = self.reference_cross_sectional_area()
        return dynamicPressure * dragCoefficient * referenceArea

    def drag_coefficient(
        self,
        noseDragCoefficient: float = None,
        bodyDragCoefficient: float = None,
        noseLength: float = None,
        bodyLength: float = None,
        cfdData: Iterable[dict] = None,
        cfdWeights: Iterable[float] = None,
        cfdBlendFactor: float = 0.5,
    ) -> float:
        """Return an estimated fuselage drag coefficient.

        External inputs may override individual part drag coefficients and lengths.
        A surrogate model can be blended from CFD drag data when provided.
        """
        # Step 1: determine drag coefficients for the nose and body
        noseCd = (
            noseDragCoefficient
            if noseDragCoefficient is not None
            else self._drag_coefficient_from_part(self.noseCone)
        )
        bodyCd = (
            bodyDragCoefficient
            if bodyDragCoefficient is not None
            else self._drag_coefficient_from_part(self.bodyContour)
        )

        # Step 2: determine lengths for the nose and body
        noseLength = (
            noseLength
            if noseLength is not None
            else self._part_length(self.noseCone)
        )
        bodyLength = (
            bodyLength
            if bodyLength is not None
            else self._part_length(self.bodyContour)
        )
        totalLength = noseLength + bodyLength

        # Step 3: compute a length-weighted average drag coefficient
        if totalLength <= 0:
            baseCd = max(noseCd, bodyCd)
        else:
            baseCd = (noseCd * noseLength + bodyCd * bodyLength) / totalLength

        # Step 4: optionally blend with surrogate CFD drag coefficient
        if cfdData is not None:
            surrogateCd = self.surrogate_drag_coefficient(cfdData, cfdWeights)
            blend = max(0.0, min(1.0, cfdBlendFactor))
            return baseCd * (1.0 - blend) + surrogateCd * blend

        return baseCd

    def surrogate_drag_coefficient(
        self,
        cfdData: Iterable[dict],
        weights: Iterable[float] = None,
    ) -> float:
        """Build a surrogate drag coefficient from CFD simulation results."""
        # Step 1: require CFD data to build the surrogate model
        if cfdData is None:
            raise ValueError("CFD data is required to build a surrogate model")

        coefficients = []
        for entry in cfdData:
            # Step 2: extract coefficient if directly available
            if isinstance(entry, dict):
                if "drag_coefficient" in entry:
                    coefficients.append(float(entry["drag_coefficient"]))
                    continue

                # Step 3: compute coefficient from drag force and flow data
                if "drag_force" in entry:
                    dragForce = float(entry["drag_force"])
                    dynamicPressure = entry.get("dynamic_pressure")
                    if dynamicPressure is None:
                        if "velocity" in entry:
                            rho = float(entry.get("air_density", 1.225))
                            velocity = float(entry["velocity"])
                            dynamicPressure = 0.5 * rho * velocity * velocity
                        else:
                            raise ValueError(
                                "CFD entry must provide 'dynamic_pressure' or 'velocity'"
                            )

                    referenceArea = float(
                        entry.get("reference_area", self.reference_cross_sectional_area())
                    )
                    coefficients.append(dragForce / (dynamicPressure * referenceArea))
                    continue

            raise ValueError(
                "Each CFD data entry must provide 'drag_coefficient' or 'drag_force'"
            )

        # Step 4: validate that coefficients were collected
        if not coefficients:
            raise ValueError("CFD data must contain at least one valid entry")

        # Step 5: set default weights when none are provided
        if weights is None:
            weights = [1.0] * len(coefficients)

        # Step 6: validate weight count matches coefficient count
        if len(weights) != len(coefficients):
            raise ValueError("Weights must match the number of CFD data entries")

        weightedSum = sum(
            float(coefficient) * float(weight)
            for coefficient, weight in zip(coefficients, weights)
        )
        totalWeight = sum(float(weight) for weight in weights)
        if totalWeight <= 0:
            raise ValueError("Total weight must be greater than zero")

        return weightedSum / totalWeight

    def _drag_coefficient_from_part(self, part: Any) -> float:
        """Extract an empirical drag coefficient from a body-part object."""
        # Step 1: use empirical_drag_coefficient() if available
        if hasattr(part, "empirical_drag_coefficient") and callable(
            part.empirical_drag_coefficient
        ):
            return part.empirical_drag_coefficient()

        # Step 2: use drag_coefficient() if available
        if hasattr(part, "drag_coefficient") and callable(part.drag_coefficient):
            return part.drag_coefficient()

        # Step 3: check for a drag_coefficient value in shape metadata
        if hasattr(part, "shape") and isinstance(part.shape, dict):
            value = part.shape.get("drag_coefficient")
            if value is not None:
                return float(value)

        # Step 4: raise if no coefficient source is found
        raise ValueError(
            "Body part must provide an empirical drag coefficient via "
            "'empirical_drag_coefficient()' or 'drag_coefficient()'"
        )

    def _part_length(self, part: Any) -> float:
        """Estimate the part length from its contour coordinates."""
        # Step 1: read the coordinates attribute or method
        points = getattr(part, "coordinates", None)
        if callable(points):
            points = points()

        # Step 2: normalize points and handle missing data
        points = self._flatten_points(points) if points is not None else []
        if not points:
            return 0.0

        # Step 3: compute the span of x coordinates as part length
        xs = [point[0] for point in points]
        return max(xs) - min(xs)
