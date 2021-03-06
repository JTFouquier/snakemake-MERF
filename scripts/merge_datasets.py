

import pandas as pd
from functools import reduce

output_folder = "random-forest/TEST/HDL/02-MERGED-DATA/"
dataset_file_list = snakemake.input["dataset_list"]

# TODO metadata-pcas needs be clear as this can be done on other datasets
# TODO add name of dataset to folder and file names to stay organized

df_list = []
df_dict = {}
for i in range(len(dataset_file_list)):
    df = pd.read_csv(dataset_file_list[i], sep="\t",
                     index_col="StudyID.Timepoint")
    df_name = 'df' + str(i)
    df_dict[df_name] = df
    df_list.append(df_dict[df_name])

# TODO VERIFY THIS MERGE *** review merge decisions ***
df = reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True,
                                  how="inner", validate="one_to_one",
                                  sort=False), df_list)
df = df.rename_axis("StudyID.Timepoint")
df["SampleID"] = df.index

df.to_csv(output_folder + "final-merged-dfs.txt", sep="\t")

