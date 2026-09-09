"""Aggregate electrical model for CircuitMind."""

from collections.abc import Iterable
from dataclasses import dataclass

from circuitmind.model.connection import ConnectionPoint, ConnectionPointOccurrence
from circuitmind.model.device import Device, DeviceOccurrence
from circuitmind.model.document import Document, DrawingPage
from circuitmind.model.net import ElectricalNet, WireSegment
from circuitmind.model.source import SourceReference


@dataclass(frozen=True, slots=True)
class CircuitModel:
    """A coherent electrical model with validated entity relationships."""

    documents: tuple[Document, ...] = ()
    pages: tuple[DrawingPage, ...] = ()
    devices: tuple[Device, ...] = ()
    device_occurrences: tuple[DeviceOccurrence, ...] = ()
    connection_points: tuple[ConnectionPoint, ...] = ()
    connection_point_occurrences: tuple[ConnectionPointOccurrence, ...] = ()
    wire_segments: tuple[WireSegment, ...] = ()
    electrical_nets: tuple[ElectricalNet, ...] = ()

    def __post_init__(self) -> None:
        document_ids = self._require_unique_ids(
            "document",
            (document.id for document in self.documents),
        )

        device_ids = self._require_unique_ids(
            "device",
            (device.id for device in self.devices),
        )

        connection_point_ids = self._require_unique_ids(
            "connection point",
            (point.id for point in self.connection_points),
        )

        wire_segment_ids = self._require_unique_ids(
            "wire segment",
            (segment.id for segment in self.wire_segments),
        )

        self._require_unique_ids(
            "device occurrence",
            (occurrence.id for occurrence in self.device_occurrences),
        )

        self._require_unique_ids(
            "connection point occurrence",
            (occurrence.id for occurrence in self.connection_point_occurrences),
        )

        self._require_unique_ids(
            "electrical net",
            (net.id for net in self.electrical_nets),
        )

        page_keys = [(page.document_id, page.page_number) for page in self.pages]

        if len(set(page_keys)) != len(page_keys):
            raise ValueError("Duplicate drawing page")

        page_key_set = set(page_keys)

        for page in self.pages:
            if page.document_id not in document_ids:
                raise ValueError(f"Drawing page references unknown document_id: {page.document_id}")

        for device_occurrence in self.device_occurrences:
            if device_occurrence.device_id not in device_ids:
                raise ValueError(
                    f"Device occurrence references unknown device_id: {device_occurrence.device_id}"
                )

            self._validate_graphical_source(
                "Device occurrence",
                device_occurrence.source,
                document_ids,
                page_key_set,
            )
        for point in self.connection_points:
            if point.device_id not in device_ids:
                raise ValueError(
                    f"Connection point references unknown device_id: {point.device_id}"
                )

        for connection_occurrence in self.connection_point_occurrences:
            if connection_occurrence.connection_point_id not in connection_point_ids:
                raise ValueError(
                    "Connection point occurrence references unknown "
                    f"connection_point_id: {connection_occurrence.connection_point_id}"
                )

            self._validate_graphical_source(
                "Connection point occurrence",
                connection_occurrence.source,
                document_ids,
                page_key_set,
            )

        for segment in self.wire_segments:
            self._validate_graphical_source(
                "Wire segment",
                segment.source,
                document_ids,
                page_key_set,
            )

        connection_point_net: dict[str, str] = {}
        wire_segment_net: dict[str, str] = {}

        for net in self.electrical_nets:
            for point_id in net.connection_point_ids:
                if point_id not in connection_point_ids:
                    raise ValueError(
                        f"Electrical net references unknown connection_point_id: {point_id}"
                    )

                previous_net = connection_point_net.get(point_id)

                if previous_net is not None:
                    raise ValueError(
                        f"Connection point {point_id} belongs to multiple electrical nets"
                    )

                connection_point_net[point_id] = net.id

            for segment_id in net.wire_segment_ids:
                if segment_id not in wire_segment_ids:
                    raise ValueError(
                        f"Electrical net references unknown wire_segment_id: {segment_id}"
                    )

                previous_net = wire_segment_net.get(segment_id)

                if previous_net is not None:
                    raise ValueError(
                        f"Wire segment {segment_id} belongs to multiple electrical nets"
                    )

                wire_segment_net[segment_id] = net.id

    @staticmethod
    def _require_unique_ids(
        entity_name: str,
        ids: Iterable[str],
    ) -> set[str]:
        seen: set[str] = set()
        duplicates: set[str] = set()

        for entity_id in ids:
            if entity_id in seen:
                duplicates.add(entity_id)

            seen.add(entity_id)

        if duplicates:
            duplicate_text = ", ".join(sorted(duplicates))
            raise ValueError(f"Duplicate {entity_name} ids: {duplicate_text}")

        return seen

    @staticmethod
    def _validate_graphical_source(
        entity_name: str,
        source: SourceReference,
        document_ids: set[str],
        page_keys: set[tuple[str, int]],
    ) -> None:
        if source.document_id not in document_ids:
            raise ValueError(f"{entity_name} references unknown document_id: {source.document_id}")

        if source.page_number is None:
            raise ValueError(f"{entity_name} must reference a drawing page")

        page_key = (source.document_id, source.page_number)

        if page_key not in page_keys:
            raise ValueError(
                f"{entity_name} references unknown drawing page: "
                f"{source.document_id} page {source.page_number}"
            )
