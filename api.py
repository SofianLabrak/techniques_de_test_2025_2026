import uuid

import requests
from flask import Flask, Response, jsonify

from point_set import PointSet
from triangulator import Triangulator

app = Flask(__name__)


class PointSetManagerError(Exception):
    pass


class PointSetNotFoundError(Exception):
    pass


def get_pointset_from_manager(point_set_id: str) -> PointSet:
    url = f"http://localhost:5001/pointset/{point_set_id}"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            raise PointSetNotFoundError("PointSet non trouvé")
        if response.status_code != 200:
            raise PointSetManagerError(
                f"Erreur du PointSetManager : {response.status_code}"
            )
        return PointSet.deserialize(response.content)
    except requests.RequestException as e:
        raise PointSetManagerError(f"Erreur de connexion : {str(e)}") from e


@app.route('/triangulation/<point_set_id>', methods=['GET'])
def triangulate(point_set_id):
    try:
        uuid.UUID(point_set_id)
    except ValueError:
        return jsonify({"error": "Format UUID invalide"}), 400

    try:
        point_set = get_pointset_from_manager(point_set_id)

        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()

        return Response(
            Triangulator.serialize_triangles(point_set, triangles),
            mimetype='application/octet-stream'
        )

    except PointSetNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except PointSetManagerError as e:
        return jsonify({"error": str(e)}), 503
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Erreur interne du serveur"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
