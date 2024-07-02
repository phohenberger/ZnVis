"""
ZnVis: A Zincwarecode package.
License
-------
This program and the accompanying materials are made available under the terms
of the Eclipse Public License v2.0 which accompanies this distribution, and is
available at https://www.eclipse.org/legal/epl-v20.html
SPDX-License-Identifier: EPL-2.0
Copyright Contributors to the Zincwarecode Project.
Contact Information
-------------------
email: zincwarecode@gmail.com
github: https://github.com/zincware
web: https://zincwarecode.com/
Citation
--------
If you use this module please cite us with:
Summary
-------
Module for the mesh parent class.
"""

from dataclasses import dataclass, field

import numpy as np
import open3d as o3d
import open3d.visualization.rendering as rendering

from znvis.material.material import Material
from znvis.transformations.rotation_matrices import rotation_matrix

@dataclass
class Mesh:
    """
    Parent class for the ZnVis meshes.

    Attributes
    ----------
    material : Material
            A ZnVis material class.
    """

    material: Material = field(default_factory=lambda: Material())
    base_direction: np.ndarray = field(default_factory=lambda: np.array([1, 0, 0]))
    dynamic_material: bool = False

    def __post_init__(self):
        """
        Post init function to create materials.
        """
        
        if not self.dynamic_material:
            material = rendering.MaterialRecord()
            material.base_color = np.hstack((self.material.colour, self.material.alpha))
            material.shader = "defaultLitTransparency"
            material.base_metallic = self.material.metallic
            material.base_roughness = self.material.roughness
            material.base_reflectance = self.material.reflectance
            material.base_anisotropy = self.material.anisotropy
            self.o3d_material = material
        else:
            self.o3d_material = np.empty(self.material.colour.shape[:2], dtype=object)
            for i in range(self.material.colour.shape[0]):
                for j in range(self.material.colour.shape[1]):
                    material = rendering.MaterialRecord()
                    material.base_color = np.hstack((self.material.colour[i, j], self.material.alpha))
                    material.shader = "defaultLitTransparency"
                    material.base_metallic = self.material.metallic
                    material.base_roughness = self.material.roughness
                    material.base_reflectance = self.material.reflectance
                    material.base_anisotropy = self.material.anisotropy
                    self.o3d_material[i, j] = material

    def instantiate_mesh(
        self, starting_position: np.ndarray, starting_orientation: np.ndarray = None, step: int = 0, particle_id: int = 0
    ) -> o3d.geometry.TriangleMesh:
        """
        Create a mesh object defined by the dataclass.

        Parameters
        ----------
        starting_position : np.ndarray shape=(3,)
                Starting position of the mesh.
        starting_orientation : np.ndarray shape=(3,) (default = None)
                Starting orientation of the mesh.

        Returns
        -------
        mesh : o3d.geometry.TriangleMesh
        """
        mesh = self.create_mesh_object()
        mesh.compute_vertex_normals()
        mesh.translate(starting_position.astype(float))
        if starting_orientation is not None:
            matrix = rotation_matrix(self.base_direction, starting_orientation)
            mesh.rotate(matrix)

        return mesh
    
    def create_mesh_object(self) -> o3d.geometry.TriangleMesh:
        """
        Create a mesh object defined by the dataclass.
        """
        raise NotImplementedError("Method not implemented.")
