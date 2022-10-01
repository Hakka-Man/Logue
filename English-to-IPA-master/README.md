

### English to IPA (eng_to_ipa)


This Python program utilizes the Carnegie-Mellon University Pronouncing Dictionary to convert English text into the [International Phonetic Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet).

### Installation ### 

1. Download this directory locally 
2. Run `python -m pip install .` in the same directory as ` setup.py`.

### Key functions ###


The `convert` function is used to take English text and convert it to IPA, like so:

```Python
>>> import eng_to_ipa as ipa
>>> ipa.convert("The quick brown fox jumped over the lazy dog.")
'ðə kwɪk braʊn fɑks ʤəmpt ˈoʊvər ðə ˈleɪzi dɔg.'
``` 

Note that words that cannot be found in the CMU dictionary are simply reprinted with an asterisk.

#### `convert` parameters

* **text** : *string* - The input string of English text to be converted to IPA notation.

* **keep_punct** : *boolean, optional (default=True)* - Determines whether or not the punctuation marks from the input string
should be retained or not.

* **retrieve_all** : *boolean, optional (default=False)* - Given that some words might have more than one transcription,
this parameter determines whether or not a list of all possible combinations of transcriptions should be returned (True)
 or just the string of one transcription (False).
 
* **stress_marks** : *string, optional (default='both')* - Determines whether or not the primary and secondary stress 
markings (ˈ, ˌ) should be retained. Understood arguments are:
   * "primary" - retains primary stress only 
   * "secondary" - retains secondary stress only
   * "both" - to keep both primary and secondary stress markers
   * "none" - preserve neither primary nor secondary stress
   
* **mode** : *string, optional (default='sql')* - Accepts "sql" or "json", depending on which version of the database you'd like to use.
 As another option for JSON users, simply use the function `jonvert` instead of `convert`. 

```Python
>>> ipa.convert("I went to Japan last summer.", retrieve_all=True, stress_marks=False)
['aɪ wɛnt tu ʤəpæn læst səmər.', 'aɪ wɛnt tə ʤəpæn læst səmər.', 'aɪ wɛnt tɪ ʤəpæn læst səmər.']
```

#### `ipa_list`

The `ipa_list` function returns a list of each word as a list of all its possible transcriptions. It has all the same
optional `stress_marks` and `keep_punct` parameters as `convert`.
```Python
>>> ipa.ipa_list("The record was expensive.")
[['ði', 'ðə'], ['rəˈkɔrd', 'rɪˈkɔrd', 'ˈrɛkərd'], ['wɑz'], ['ɪkˈspɛnsɪv.']]
```
   
#### `isin_cmu`

The `isin_cmu` function takes a word (or list of words) and checks if it is in the CMU pronouncing dictionary (returns 
`True` or `False`). If a list of words is provided, then `True` will only be returned if *every* provided word is in the dictionary.

```Python
>>> ipa.isin_cmu("The dentist opened a new practice.")
True
>>> ipa.isin_cmu("emoji")
False
```
   
#### `get_rhymes`

The `get_rhymes` function returns a list of rhymes for a word or set of words. 
```Python
>>> ipa.get_rhymes("rhyming function")
[['climbing', 'diming', 'liming', 'priming', 'timing'], ['compunction', 'conjunction', 'dysfunction', 'injunction', 'junction', 'malfunction']]
```
*Use the `jhymes` function instead to force usage of the JSON database.*
   
#### `syllable_count`

The `syllable_count` function returns an integer, corresponding to the number of syllables in a word. Returns a list of 
syllable counts if more than one word is provided in the input string.

```Python
>>> ipa.syllable_count("computer programming")
[3, 3]
```

### Other Resources

For another Python package that offers support for rhyming and syllable counts (as well as other cool things), see [pronouncingpy](https://github.com/aparrish/pronouncingpy).
