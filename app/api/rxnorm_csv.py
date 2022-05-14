import pandas as pd 

def download_rxnorm(data_dir="../data/", output_format="feather"):
    """
    Download RxNorm data for *currently prescribable* drugs. The RxNorm data 
    describes a standard identifier for drugs, along with commonly used names, 
    ingredients and relationships. The full data set is very large and requires a  
    special licence. Here, we use the subset of drugs that can currently be 
    prescribed, which are available without licence. We are also going to ignore 
    the relational data and focus on commonly used identifiers and the RxNorm ID.
    Parameters
    ----------
    data_dir : string
       The path to the directory where the data should be stored.
    output_format : string, optional, default: "feather"
       The file format for the output file. Currently supported data formats are:
            * "cvs": return comma-separated values in a simple ASCII file
            * "feather": return a `.feather` file (required `feather` Python package!)
    """
    # URL to the data file
    url = "https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_01032017.zip"

    # download data from NIH:
    _download_data(url, data_dir=data_dir, data_name="rxnorm.zip", zipped_data=True)


    # Column names as copied from the NIH website
    names = ["RXCUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "RXAUI",
         "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", "SUPPRESS", "CVF"]

    # we only want column 0 (the RXCUI identifier) and 14 (the commonly used name)
    rxnorm = pd.read_csv(data_dir + "rrf/RXNCONSO.RRF", sep="|", names=names, index_col=False,
                         usecols=[0,14])
 
    # make all strings lowercase
    rxnorm["STR"] = rxnorm["STR"].str.lower()

    if output_format == "csv":
        # get all the column names for the file header
        hdr = list(rxnorm.columns)
        # add a `#` to the first element of the list so header 
        # won't be confused for data
        hdr[0] = "#" + hdr[0]
        rxnorm.to_csv(data_dir + "rxnorm.csv", sep="\t", header=hdr,
                               index=False)
    elif output_format == "feather":
        # write the results to a feather file:
        feather.write_dataframe(rxnorm, data_dir + 'rxnorm.feather')
    else:
        raise OptionUndefinedError()

    return