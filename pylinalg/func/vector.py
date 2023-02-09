import numpy as np


def vector_normalize(vectors, /, *, out=None, dtype=None):
    """
    Normalize an array of vectors.

    Parameters
    ----------
    vectors : array_like, [..., 3]
        array of vectors
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    ndarray, [..., 3]
        array of normalized vectors.
    """
    vectors = np.asarray(vectors)
    if out is None:
        out = np.empty_like(vectors, dtype=dtype)
    return np.divide(vectors, np.linalg.norm(vectors, axis=-1)[:, None], out=out)


def vector_make_homogeneous(vectors, /, *, w=1, out=None, dtype=None):
    """
    Append homogeneous coordinates to vectors.

    Parameters
    ----------
    vectors : array_like, [..., 3]
        array of vectors
    w : number, optional, default is 1
        the value for the homogeneous dimensionality.
        this affects the result of translation transforms. use 0 (vectors)
        if the translation component should not be applied, 1 (positions)
        otherwise.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    ndarray, [..., 4]
        The list of vectors with appended homogeneous value.
    """
    vectors = np.asarray(vectors)
    shape = list(vectors.shape)
    shape[-1] += 1
    if out is None:
        out = np.empty_like(vectors, shape=shape, dtype=dtype)
    out[..., -1] = w
    out[..., :-1] = vectors
    return out


def vector_apply_matrix(vectors, matrix, /, *, w=1, out=None, dtype=None):
    """
    Transform vectors by a transformation matrix.

    Parameters
    ----------
    vectors : ndarray, [..., 3]
        Array of vectors
    matrix : ndarray, [4, 4]
        Transformation matrix
    w : number, optional, default 1
        The value for the homogeneous dimensionality.
        this affects the result of translation transforms. use 0 (vectors)
        if the translation component should not be applied, 1 (positions)
        otherwise.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    ndarray, [..., 3]
        transformed vectors
    """
    vectors = vector_make_homogeneous(vectors, w=w)
    # usually when applying a transformation matrix to a vector
    # the vector is a column, so if you were to have an array of vectors
    # it would have shape (ndim, nvectors).
    # however, we instead have the convention (nvectors, ndim) where
    # vectors are rows.
    # therefore it is necessary to transpose the transformation matrix
    # additionally we slice off the last row of the matrix, since we are not interested
    # in the resulting w coordinate
    transform = matrix[:-1, :].T
    if out is not None:
        try:
            # if `out` is exactly compatible, that is the most performant
            return np.dot(vectors, transform, out=out)
        except ValueError:
            # otherwise we need a temporary array and cast
            out[:] = np.dot(vectors, transform)
            return out
    # otherwise just return whatever dot computes
    out = np.dot(vectors, transform)
    # cast if requested
    if dtype is not None:
        out = out.astype(dtype, copy=False)
    return out


def vector_unproject(vector, matrix, /, *, depth=0, out=None, dtype=None):
    """
    Un-project a vector from 2D space to 3D space.

    Find a ``vectorB`` in 3D euclidean space such that the projection
    ``matrix @ vectorB`` yields the provided vector (in 2D euclidean
    space). Since the solution to the above is a 1D subspace of 3D space (a
    line), ``depth`` is used to select a single vector within.

    Parameters
    ----------
    vector : ndarray, [2]
        The vector to be un-projected.
    matrix: ndarray, [4, 4]
        The camera's intrinsic matrix.
    depth : number, optional
        The distance of the unprojected vector from the camera.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    projected_vector : ndarray, [3]
        The unprojected vector in 3D space
    """

    raise NotImplementedError()


def vector_apply_quaternion_rotation(vector, quaternion, /, *, out=None, dtype=None):
    """Rotate a vector using a quaternion.

    Parameters
    ----------
    vector : ndarray, [3]
        The vector to be rotated.
    quaternion : ndarray, [4]
        The quaternion to apply (in xyzw format).
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    rotated_vector : ndarray, [3]
        The rotated vector.

    """

    raise NotImplementedError()


def vector_spherical_to_euclidean(spherical, /, *, out=None, dtype=None):
    """Convert spherical -> euclidian coordinates.

    Parameters
    ----------
    spherical : ndarray, [3]
        A vector in spherical coordinates (r, phi, theta).
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    euclidean : ndarray, [3]
        A vector in euclidian coordinates.

    """

    raise NotImplementedError()


def vector_distance_between(vector_a, vector_b, /, *, out=None, dtype=None):
    """The distance between two vectors

    Parameters
    ----------
    vector_a : ndarray, [3]
        The first vector.
    vector_b : ndarray, [3]
        The second vector.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    distance : ndarray
        The distance between both vectors.

    """

    raise NotImplementedError()


def vector_from_matrix_position(homogeneous_matrix, /, *, out=None, dtype=None):
    """Position component of a homogeneous matrix.

    Parameters
    ----------
    homogeneous_matrix : ndarray, [4, 4]
        The matrix of which the position/translation component will be
        extracted.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    position : ndarray, [3]
        The position/translation component.

    """

    raise NotImplementedError()


def vector_euclidean_to_spherical(euclidean, /, *, out=None, dtype=None):
    """Convert euclidean -> spherical coordinates

    Parameters
    ----------
    euclidean : ndarray, [3]
        A vector in euclidean coordinates.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    spherical : ndarray, [3]
        A vector in spherical coordinates (r, phi, theta).

    """

    euclidean = np.asarray(euclidean, dtype=float)

    if out is None:
        out = np.zeros_like(euclidean, dtype=dtype)
    else:
        out[:] = 0

    out[..., 0] = np.sqrt(np.sum(euclidean**2, axis=-1))

    # choose phi = 0 if vector runs along y-axis
    len_xz = np.sum(euclidean[..., [0, 2]] ** 2, axis=-1)
    xz_nonzero = ~np.all(len_xz == 0, axis=-1)
    out[..., 1] = np.divide(euclidean[..., 2], np.sqrt(len_xz), where=xz_nonzero)
    out[..., 1] = np.sign(euclidean[..., 0]) * np.arccos(out[..., 1], where=xz_nonzero)

    # choose psi = 0 at the origin (0, 0, 0)
    r_zero = np.all(out[..., [0]] == 0, axis=-1)
    out[..., 2] = np.divide(euclidean[..., 2], out[..., 0], where=~r_zero)
    out[..., 2] = np.arccos(out[..., 2], where=~r_zero)

    return out


def vector_make_spherical_safe(vector, /, *, out=None, dtype=None):
    """Normalize sperhical coordinates.

    Normalizes a vector of spherical coordinates to restrict phi to (eps, pi-eps) and
    theta to (0, 2pi).

    Parameters
    ----------
    vector : ndarray, [3]
        A vector in spherical coordinates.
    out : ndarray, optional
        A location into which the result is stored. If provided, it
        must have a shape that the inputs broadcast to. If not provided or
        None, a freshly-allocated array is returned. A tuple must have
        length equal to the number of outputs.
    dtype : data-type, optional
        Overrides the data type of the result.

    Returns
    -------
    normalized_vector : ndarray, [3]
        A vector in spherical coordinates with restricted angle values.

    """

    raise NotImplementedError()
