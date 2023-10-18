import numpy as np
import pandas as pd

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from evadb.utils.generic_utils import try_to_import_cv2


class BlurImage(AbstractFunction):
    @setup(cacheable=False, function_type="cv2-transformation", batchable=True)
    def setup(self):
        try_to_import_cv2()

    @property
    def name(self):
        return "invertblurImage"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["data"],
                column_types=[NdArrayType.FLOAT32],
                column_shapes=[(None, None, 3)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["invertblurframe"],
                column_types=[NdArrayType.FLOAT32],
                column_shapes=[(None, None)],
            )
        ],
    )
    def forward(self, frame1: pd.DataFrame) -> pd.DataFrame:
        def InvertBlurImage(row: pd.Series) -> np.ndarray:
            row = row.to_list()
            frame = row[0]

            import cv2

            frame = cv2.bitwise_not(frame)

            return frame

        ret = pd.DataFrame()
        ret["invertblurframe"] = frame1.apply(InvertBlurImage, axis=1)
        return ret