from dateutil.parser import parse

from river_flows.data.site_condition import BatchSiteConditions, SiteCondition


def test__batch_values__success():
    # Arrange / Act
    batch = BatchSiteConditions(site_conditions=_build_site_conditions(8000))

    # Assert
    assert len(batch.batch_site_conditions) == 2
    assert all(isinstance(batch, list) for batch in batch.batch_site_conditions)
    assert all(
        isinstance(conditions, SiteCondition)
        for conditions in batch.batch_site_conditions[0]
    )


def _build_site_conditions(count: int) -> list[SiteCondition]:
    site_conditions = []

    for i in range(count):
        site_condition = SiteCondition(
            site_id="FAKE_SITE_ID",
            site_name="FAKE_SITE_NAME",
            timestamp=parse("2024-05-01T00:00"),
            value=100.0,
            unit="ft3/s",
        )
        site_conditions.append(site_condition)

    return site_conditions
