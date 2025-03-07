from unittest.mock import Mock, patch

from app.common import path
from app.common.test import BaseApiTest

ENCODED_VAR = "var%20name"


class DatasetsTest(BaseApiTest):

    DATASETS = [
        {
            "ds_id": 1,
            "title": "Test dataset",
            "is_raster": True,
            "shared_id": "test_dataset",
        }
    ]

    @patch(
        "app.common.client.get_dataset_list",
        new=Mock(return_value=DATASETS),
    )
    def testGetAllDatasets(self):
        response = self.client.get("api/datasets/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), len(DatasetsTest.DATASETS))

        for index, ref in enumerate(DatasetsTest.DATASETS):
            data = response.json[index]
            for k, v in ref.items():
                self.assertIn(k, data)
                self.assertEqual(v, data[k])

            self.assertIn("openaireLink", data)
            self.assertTrue(
                data["openaireLink"].startswith(
                    "https://enermaps.openaire.eu/search/dataset?datasetId=enermaps____"
                )
            )

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/")
        self.assertEqual(response.status_code, 405)


class DatasetsFullTest(BaseApiTest):

    DATASETS = [
        {
            "ds_id": 1,
            "title": "Test dataset",
            "is_raster": True,
            "shared_id": "test_dataset",
        }
    ]

    VARIABLES = {
        "variables": ["var1", "var2"],
        "time_periods": [2000],
        "temporal_granularity": "custom",
        "start_at": "2000-01-01 00:00",
        "end_at": None,
        "default_parameters": {},
    }

    @patch(
        "app.common.client.get_dataset_list",
        new=Mock(return_value=DATASETS),
    )
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=VARIABLES),
    )
    def testGetAllDatasets(self):
        response = self.client.get("api/datasets/full/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), len(DatasetsTest.DATASETS))

        for index, ref in enumerate(DatasetsTest.DATASETS):
            data = response.json[index]
            for k, v in ref.items():
                if k != "info":
                    self.assertIn(k, data)
                    self.assertEqual(v, data[k])
                else:
                    for k2, v2 in DatasetsTest.VARIABLES.items():
                        self.assertIn(k2, v)
                        self.assertEqual(v2, v[k])

            self.assertIn("openaireLink", data)
            self.assertTrue(
                data["openaireLink"].startswith(
                    "https://enermaps.openaire.eu/search/dataset?datasetId=enermaps____"
                )
            )

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/full/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/full/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/full/")
        self.assertEqual(response.status_code, 405)


class DatasetParametersTest(BaseApiTest):

    PARAMETERS_FULL = {
        "variables": ["var1", "var2"],
        "time_periods": [2000],
        "temporal_granularity": "custom",
        "start_at": "2000-01-01 00:00",
        "end_at": None,
        "default_parameters": {},
    }

    PARAMETERS_EMPTY_TIME_PERIODS = {
        "variables": ["var1", "var2"],
        "time_periods": [],
        "temporal_granularity": "custom",
        "start_at": "2000-01-01 00:00",
        "end_at": None,
        "default_parameters": {},
    }

    PARAMETERS_EMPTY_VARS = {
        "variables": [],
        "time_periods": [2000],
        "temporal_granularity": "custom",
        "start_at": "2000-01-01 00:00",
        "end_at": None,
        "default_parameters": {},
    }

    PARAMETERS_EMPTY = {
        "variables": [],
        "time_periods": [],
        "temporal_granularity": "custom",
        "start_at": "2000-01-01 00:00",
        "end_at": None,
        "default_parameters": {},
    }

    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=PARAMETERS_FULL),
    )
    def testGetParametersComplete(self):
        response = self.client.get("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, DatasetParametersTest.PARAMETERS_FULL)

    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=PARAMETERS_EMPTY_TIME_PERIODS),
    )
    def testGetParametersWithoutTimePeriods(self):
        response = self.client.get("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, DatasetParametersTest.PARAMETERS_EMPTY_TIME_PERIODS
        )

    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=PARAMETERS_EMPTY_VARS),
    )
    def testGetVParametersWithoutVariables(self):
        response = self.client.get("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, DatasetParametersTest.PARAMETERS_EMPTY_VARS)

    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=PARAMETERS_EMPTY),
    )
    def testGetParametersWithoutContent(self):
        response = self.client.get("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, DatasetParametersTest.PARAMETERS_EMPTY)

    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=None),
    )
    def testGetParametersOfUnknownDataset(self):
        response = self.client.get("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 404)

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/1/parameters/")
        self.assertEqual(response.status_code, 405)


class AreasTest(BaseApiTest):
    def testGetAllAreas(self):
        response = self.client.get("api/datasets/areas/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), 5)

        for area in response.json:
            self.assertIn("id", area)
            self.assertIn("title", area)

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/areas/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/areas/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/areas/")
        self.assertEqual(response.status_code, 405)


class VectorLayerNameTest(BaseApiTest):
    def testIdOnly(self):
        response = self.client.get("api/datasets/layer_name/vector/42/")
        name = path.make_unique_layer_name(path.VECTOR, 42)
        self.assertEqual(name, response.data.decode())

    def testWithVariable(self):
        response = self.client.get(f"api/datasets/layer_name/vector/42/{ENCODED_VAR}/")
        name = path.make_unique_layer_name(path.VECTOR, 42, variable="var name")
        self.assertEqual(name, response.data.decode())

    def testWithTimePeriod(self):
        response = self.client.get("api/datasets/layer_name/vector/42/-/2015/")
        name = path.make_unique_layer_name(path.VECTOR, 42, time_period=2015)
        self.assertEqual(name, response.data.decode())

    def testWithVariableAndTimePeriod(self):
        response = self.client.get(
            f"api/datasets/layer_name/vector/42/{ENCODED_VAR}/2015/"
        )
        name = path.make_unique_layer_name(
            path.VECTOR, 42, variable="var name", time_period=2015
        )
        self.assertEqual(name, response.data.decode())

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/layer_name/vector/42/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/layer_name/vector/42/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/layer_name/vector/42/")
        self.assertEqual(response.status_code, 405)


class RasterLayerNameTest(BaseApiTest):
    def testIdOnly(self):
        response = self.client.get("api/datasets/layer_name/raster/42/")
        name = path.make_unique_layer_name(path.RASTER, 42)
        self.assertEqual(name, response.data.decode())

    def testWithVariable(self):
        response = self.client.get(f"api/datasets/layer_name/raster/42/{ENCODED_VAR}/")
        name = path.make_unique_layer_name(path.RASTER, 42, variable="var name")
        self.assertEqual(name, response.data.decode())

    def testWithTimePeriod(self):
        response = self.client.get("api/datasets/layer_name/raster/42/-/2015/")
        name = path.make_unique_layer_name(path.RASTER, 42, time_period=2015)
        self.assertEqual(name, response.data.decode())

    def testWithVariableAndTimePeriod(self):
        response = self.client.get(
            f"api/datasets/layer_name/raster/42/{ENCODED_VAR}/2015/"
        )
        name = path.make_unique_layer_name(
            path.RASTER, 42, variable="var name", time_period=2015
        )
        self.assertEqual(name, response.data.decode())

    def testPostNotAllowed(self):
        response = self.client.post("api/datasets/layer_name/raster/42/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/datasets/layer_name/raster/42/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/datasets/layer_name/raster/42/")
        self.assertEqual(response.status_code, 405)


class GeoJSONTest(BaseApiTest):

    GEOJSON = {
        "type": "FeatureCollection",
        "features": [
            {"id": "FID1", "type": "Feature", "geometry": None, "properties": {}}
        ],
    }

    @patch(
        "app.common.client.get_geojson",
        new=Mock(return_value=GEOJSON),
    )
    def testSuccess(self):
        response = self.client.get("api/datasets/geojson/vector%2F42/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, GeoJSONTest.GEOJSON)

    @patch(
        "app.common.client.get_geojson",
        new=Mock(return_value=None),
    )
    def testFailure(self):
        response = self.client.get("api/datasets/geojson/vector%2F42/")
        self.assertEqual(response.status_code, 404)
