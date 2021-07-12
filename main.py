# ankekat1000
# App for Applying DIKI
# ----------------------------------- imports ------------------------------------#

import streamlit as st
import pandas as pd
from nltk.tokenize import WhitespaceTokenizer



# ----------------------------------- Functions ------------------------------------#

def getDictionary(dictionary):
    if dictionary == 'DIKI small':
        chosen_dictionary = pd.read_csv("./Dictionaries/diki_small_low.txt", sep="\t")
    elif dictionary == 'DIKI large':
        chosen_dictionary = pd.read_csv("./Dictionaries/diki_small_low.txt", sep="\t")


    return chosen_dictionary



# ----------------------------------- Sidebar ------------------------------------#

def main():
    st.sidebar.header("About the DIKI App")
    st.sidebar.markdown("The DIKI Web App is a simple, web-based Tool to apply the Dictionary DIKI for Incivility Detection in German Online Discussions.")
    st.sidebar.markdown(":green_heart: Please read our [paper](https://github.com/ankekat1000/DIKI-Web-App/tree/main/Dictionaries) to get more information about DIKI and the matching algorithm.")
    #st.sidebar.info("Stoll, A., Ziegele, M., & Wilms, L. (2021): Developing an Incivility-Dictionary for German Online Discussions - A Semi-Automated Approach Combining Human and Artificial Knowledge")

    st.sidebar.markdown(":blue_heart: If you want to implement DIKI individually, you can [download DIKI from GitHub](https://github.com/ankekat1000/DIKI-Web-App/tree/main/Dictionaries)")
    st.sidebar.markdown(":purple_heart: We are looking foward to your questions and comments! Please leave us a message on the [discussion section on GitHub](https://github.com/ankekat1000/DIKI-Web-App/discussions/1).")

    st.sidebar.info("Maintained by Anke Stoll, Institute of Social Sciences @ Heinrich Heine University Düsseldorf, Germany")
    st.sidebar.text("Built with Streamlit")



# ----------------------------------- Page ------------------------------------#

    st.title("DIKI WEB APP")
    st.markdown("Welcome :hearts:")
    # ---------- Data Uplaod -------------#
    st.subheader("Upload your Data")
    st.markdown("Klick on the button `Browse files` below to upload a data file with user comments, Tweets, etc. from your computer. Make sure, your data is comma seperated, e.g., a file in .csv-format.")

    #If you want to test the app, you can download an example data file of user comments `testdata_for_diki.csv` from the [DIKI GitHub repository](https://github.com/ankekat1000/DIKI-Web-App).")
    data = st.file_uploader("Must be comma seperated data (e.g. a .csv-file).", type=["csv", "txt"])

    if data is not None:
        data.seek(0)
        df = pd.read_csv(data)
        #st.success("You selected {}".format(data))
        # ---------- Data Check -------------#
        st.markdown("Klick on the button `Show Data Frame Infos` below to display some infos about the data you uploaded or quick jump to Step 2 by selecting the box `Continue the Analysis`.")
        if st.button("Show Data Frame Infos"):

            st.write("Your data frame contains", len(df), "rows.")
            st.write("And", len(df.columns), "columns.")
            st.write("These are the first 10 rows of your data frame", df.head(10))

        else:
            pass

        # ---------- Select a Column -------------#
        if st.checkbox("Continue the Analysis"):
            st.subheader("Step 2: Select a text column to analyze.")
            column_names= list(df.columns)
            st.markdown("Now select a column in your data frame you want to analyse. Make sure, it is a column that contains text only such as comment messages, review texts, or news articles.")
            option = st.selectbox('It has to be a text column.',column_names)
            st.success("You selected {}".format(option))
            st.write(df[option].head())


        # ---------- Select a Dictionary -------------#


            if st.checkbox("Klick to next Step: Select a Dictionary"):

                st.subheader("Step 3: Select a Dictionary")
                dictionary = st.selectbox('select a dictionary', ["DIKI small", "DIKI large"])
                st.success("You selected {}".format(dictionary))

                dic = getDictionary(dictionary)
                if st.button("Show Dictionary Infos"):
                    st.write("The dictionary contains", len(dic), "entries.")
                    st.write("These are the first 10 entries of the dictionary", dic.head(10))
                else:
                    pass

                # ---------- Analysis -------------#
                if st.checkbox("Klick to next Step: Analyze!"):
                    st.subheader("Step 4: Analysis")

                    def match_unigrams_dici(X):
                        tokenizer = WhitespaceTokenizer()
                        match = []
                        X = str(X)  # vorsichtshalber
                        X = str.lower(X)
                        tokens = tokenizer.tokenize(X)

                        for token in tokens:
                            if token in dic:
                                match.append(token)
                        match = ", ".join(match)

                        return (match)


                    df["Matches"]=df[option].apply(lambda x: match_unigrams_dici(x))

                    # from nltk.tokenize import WhitespaceTokenizer
                    tokenizer = WhitespaceTokenizer()

                    # Returns number of matches (integer)

                    def match_count_unigrams(X):

                        X = str(X)  # vorsichtshalber
                        X = str.lower(X)

                        tokens = tokenizer.tokenize(X)

                        match_counts = []

                        for token in tokens:
                            if token in dic:
                                match_counts.append(token)

                        counts = len(match_counts)

                        return (counts)

                    df["Number_Matches"] = df[option].apply(lambda x: match_count_unigrams(x))

                    st.markdown("Now, the entries of the Dikionary are matches with the texts from the column from your data file you selected. \
                    For every row, you will receive the information how many and which words are matched. Therefore, two new columns will be added to your dataframe: *Matches* and *Number_Matches*." )
                    if st.checkbox("Got it, show me results!"):
                        no_matches = len(df[(df['Number_Matches']>0)])
                        st.success("Number of machted rows: {}".format(no_matches))
                        st.markdown("We added two columns to your data frame: `Matches` and `Number_Matches`")
                        st.write("First 10 columns of your data:", df.head(10))

                        if st.button('Save'):
                            df.to_csv("saved_data.csv")
                        elif st.button('Save only matched instances'):
                            if no_matches >= 1:

                                df.to_csv("saved_data_matched_instances.csv", index=None)
                            else:
                                st.markdown("There are no matches to be saved in your data file :grimacing:")


if __name__ == '__main__':
	main()