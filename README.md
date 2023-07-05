---
component-id: rulebased-postocr-corrector
name: Rule-based Post-OCR Corrector
description: Plain text files pre-processing script for correcting major OCR errors
type: TBD
release-date: 05/07/2023
release-number: v0.1
work-package: 
- WP4
licence: CC-BY_v4
links:
- https://github.com/polifonia-project/rulebased-postocr-corrector
credits:
- https://github.com/arianna-graciotti
---

# Post-OCR Correction Rules

[Polifonia Knowledge Extractor](https://github.com/polifonia-project/Polifonia-Knowledge-Extractor) entails a documents pre-processing step designed for correcting major OCR errors. This repository includes the code implemented for this purpose. The code was written considering the outcomes of a qualitative analysis of the issues caused by the transformation of the historical documents available in PDF or image format into processable formats (plain text). We focused on those documents that we treated through the *ad hoc* [OCR pipeline](https://github.com/polifonia-project/textual-corpus-population) that we implemented for the [Polifonia Textual Corpus](https://github.com/polifonia-project/Polifonia-Corpus).

We reviewed the most prominent post-OCR correction approaches based on recent surveys. In parallel, we manually evaluated pairs of original images and OCRed texts. We first aimed to qualitatively identify macro-issues that could negatively impact the processing by the Text2AMR step of the [Polifonia Knowledge Extractor](https://github.com/polifonia-project/Polifonia-Knowledge-Extractor). As The input unit to the Text2AMR parsing step, as implemented in our pipeline, is the sentence, we paid specific attention to issues in source texts that impacted sentence cohesion. We noticed that periodicals' format peculiarities, such as the arrangement of text into two or more columns on a single page, systematically caused incorrect sentence break issues.

Driven by the hypothesis that reconstructing sentence cohesion could enhance the output quality of our Text2AMR parsing step, we decided to implement a minimal rule-based strategy. This strategy, implemented as a regular expression-based substitution heuristics in a [Python script](https://github.com/arianna-graciotti/rulebased_postocr_corrector/blob/main/script/postocr_rulebased_corrector.py) released in this repository, supported the reconstruction of sentence cohesion while preserving source text paragraph breaks. 

The script contains a function that takes as input: - the path of a folder containing .txt files, - the path of the folder in which the user wants to save the output files, - the language of the input .txt files ('EN', 'ES', 'FR', 'IT'). We describe the heuristics implemented in the script in the following paragraphs.

## Sentence Cohesion Reconstruction Heuristics

1. **Dehyphenation:** We applied de-hyphenation (hyphens removal) at the beginning and end of line boundaries. Valid hyphenated words may have their hyphen removed by this process. Here are examples before and after de-hyphenation:
   - Before: 
     ```
     music, that it cannot be thought out of place in the biogra-
     phical department of our work. We might almost plead
     ```
   - After: 
     ```
     music, that it cannot be thought out of place in the biographical department of our work.
     ```

2. **Pipes removal:** We removed pipes at the beginning and end of line boundaries. Here are examples of before and after pipes removal:
   - Before: 
     ```
     Indeed |
     we have very little fault to find.
     ```
   - After: 
     ```
     Indeed we have very little fault to find.
     ```

3. **Redundant line-breaks resolution:** We removed line breaks when considered redundant and compromising single sentence cohesion. We made sure to preserve paragraph breaks. Line breaks were considered redundant when the following conditions were met:
   - Two contiguous lines *a* and *b* are separated by a single line break and line *a* does not end with a full stop.
   - Two contiguous lines *a* and *b* are separated by a single line break and line *a* ends with *Mr.*, *Mrs.* or *Miss.*
   
   - Example of text before the application of the redundant line-breaks removal heuristic:
     ```
     For one
     year Metastasio applied himself with so much diligence to the labours imposed upon him by Paglietti
     ```
   - Example of text after the application of the redundant line-breaks removal heuristic:
     ```
     For one year Metastasio applied himself with so much diligence to the labours imposed upon him by Paglietti
     ```

4. **Other Sentence Denoising Heuristics**
   
   a. **Low-ambiguity 'UFO' characters removal:** We removed the special characters `=`, `_`, `©`, `~`, `\`, `]`, `¢`, `{`, `}`, `&`, `/`, `§`, `#`, `™`, `[`, `>`, `¥`, `<`, `%`, `®`, `€`, `*` when they were preceded and followed by a space character. Being strictly preceded and followed by a space character made the identified characters less ambiguous and safer to be removed.
      
      - Example of text before the application of the 'UFO' characters removal heuristic:
        ```
        To his
        brother, too, he writes ¢ ‘ Poor Marianna never will return,
        “and the rest of my life must be wretched, insipid, and sor-
        rowful.’
        ```
      
      - Example of text after the application of the redundant line-breaks removal heuristic:
        ```
        To his brother, too, he writes ‘ Poor Marianna never will return, “and the rest of my life must be wretched, insipid, and sorrowful.’
        ```

   b. **Page number-only lines removal:** We removed lines containing only a number, which in periodicals issues corresponds to a page number. Below, examples of text before and after the application of the page number-only lines removal:
      - Before: 
        ```
        His other poetical works, which are very numerous,
        95
        are all replete with elegance, and every beauty of numbers
        which the language of Italy so sweetly supplies
        ```
      - After: 
        ```
        His other poetical works, which are very numerous, are all replete with elegance, and every beauty of numbers which the language of Italy so sweetly supplies.
        ```

   c. **Extra space characters removal:** We removed space characters between the words of a sentence when they were more than one.


