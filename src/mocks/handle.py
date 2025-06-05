import re
import json
import time

# latex = r"""
# \begin{table*}[]
# \caption{English evaluation of English queries in \benchmark{} of 8 programming languages. `Corr.' denotes the correctness of the model-generated response, and `Instr.' denotes the instruction-following accuracy of the response. The underlined values are the maximum in each column within each colored subgroup.}
# \resizebox{1.0\textwidth}{!}{
# \begin{tabular}{lc|cccccccccccccccccc}
# \toprule
# \multirow{2}{*}{Models}  & \multirow{2}{*}{Params} & \multicolumn{2}{c}{Python} & \multicolumn{2}{c}{Java} & \multicolumn{2}{c}{Cpp} & \multicolumn{2}{c}{C-sharp} & \multicolumn{2}{c}{Typescript} & \multicolumn{2}{c}{Javascript} & \multicolumn{2}{c}{Php} & \multicolumn{2}{c}{Shell} & \multicolumn{2}{c}{Avg.} \\ \cmidrule{3-20} 
#  &    & Corr.       & Instr.       & Corr.      & Instr.      & Corr.      & Instr.     & Corr.        & Instr.       & Corr.         & Instr.         & Corr.         & Instr.         & Corr.      & Instr.     & Corr.       & Instr.      & Corr.      & Instr.      \\ \midrule
# \multicolumn{20}{c}{\textit{Closed-source LLMs}}   \\ \midrule
# \rowcolor{cyan!15} Claude-3.5-Sonnet  & \faLock{}   &  48.6 & 26.7 & 33.3 & 10.8 & 19.0 & 9.0 & 12.6 & 2.9 & 24.0 & 25.0 & 48.0 & 32.0 & 41.0 & 20.0 & 28.0 & 34.0 & 31.9 & 20.0 \\  
# \rowcolor{cyan!15} Claude-3.7-Sonnet  & \faLock{}   &  47.6 & 31.4 & \underline{37.3} & 7.8 & \underline{29.0} & 6.0 & 16.5 & 3.9 & 29.0 & \underline{28.0} & 54.0 & 34.0 & \underline{59.0} & 27.0 & 36.0 & 43.0 & 38.5 & 22.6  \\  
# \rowcolor{cyan!15} GPT-4o  & \faLock{}   &   45.7 & \underline{36.2} & 25.5 & 5.9 & 22.0 & 5.0 & 15.5 & 3.9 & 30.0 & 25.0 & 47.0 & 26.0 & 51.0 & 18.0 & 32.0 & 44.0 & 33.6 & 20.5 \\
# \rowcolor{cyan!15} GPT-4o-mini  & \faLock{}   &  49.5 & 30.5 & 27.5 & 10.8 & 10.0 & 5.0 & 7.8 & \underline{5.8} & 29.0 & 25.0 & 47.0 & 27.0 & 42.0 & 22.0 & 23.0 & 44.0 & 29.5 & 21.2 \\
# \rowcolor{cyan!15} GPT-4.1  & \faLock{}   &  50.5 & 31.4 & 36.3 & 12.7 & 27.0 & 6.0 & 1.0 & 3.9 & 30.0 & 27.0 & \underline{58.0} & 25.0 & 58.0 & 26.0 & \underline{40.0} & 52.0 & 36.8 & 23.0\\
# \rowcolor{cyan!15} GPT-4.1-mini  & \faLock{}   &  46.7 & 34.3 & 35.3 & 7.8 & 23.0 & 4.0 & 0.0 & 2.9 & 27.0 & 23.0 & 57.0 & \underline{30.0} & 50.0 & 29.0 & 38.0 & \underline{53.0} & 34.6 & 23.0 \\
# \rowcolor{cyan!15} o1-mini  & \faLock{}   &    \underline{58.1} & 32.4 & 30.4 & 12.7 & \underline{29.0} & \underline{9.0} & \underline{17.5} & 2.9 & \underline{34.0} & 25.0 & 55.0 & 28.0 & 53.0 & \underline{31.0} & 37.0 & 47.0 & \underline{39.3} & \underline{23.5} \\
# \rowcolor{cyan!15} o3-mini  & \faLock{}   &    \underline{58.1} & 32.4 & 30.4 & 12.7 & \underline{29.0} & \underline{9.0} & \underline{17.5} & 2.9 & \underline{34.0} & 25.0 & 55.0 & 28.0 & 53.0 & \underline{31.0} & 37.0 & 47.0 & \underline{39.3} & \underline{23.5} \\
# \rowcolor{cyan!15} o4-mini  & \faLock{}   &    \underline{58.1} & 32.4 & 30.4 & 12.7 & \underline{29.0} & \underline{9.0} & \underline{17.5} & 2.9 & \underline{34.0} & 25.0 & 55.0 & 28.0 & 53.0 & \underline{31.0} & 37.0 & 47.0 & \underline{39.3} & \underline{23.5} \\
# \rowcolor{cyan!15} grok-3  & \faLock{}   &  25.7 & 29.5 & 18.6 & \underline{13.7} & 2.0 & 6.0 & 0.0 & 3.9 & 4.0 & 19.0 & 44.0 & 21.0 & 43.0 & 24.0 & 16.0 & 33.0 & 19.1 & 18.8 \\
# \rowcolor{cyan!15} grok-3-mini-fast  & \faLock{}   & 9.5 & 34.3 & 29.4 & 10.8 & 21.0 & 5.0 & 1.9 & 3.9 & 28.0 & 24.0 & 53.0 & 29.0 & 33.0 & 4.0 & 14.0 & 23.0 & 28.8 & 16.8 \\
# \midrule
# \multicolumn{20}{c}{\textit{0.5B+ Open-source LLMs}}     \\ \midrule
# \rowcolor{olive!15} Deepseek-Coder & 1.3B &   24.8 & 17.1 & \underline{19.6} & 2.0 & 16.0 & 3.0 & 0.0 & 1.9 & 0.0 & 1.0 & 22.0 & 13.0 & 10.0 & 3.0 & 4.0 & 9.0 & 12.1 & 6.3            \\ 
# \rowcolor{olive!15} Qwen2.5-Coder &   0.5B &  18.1 & 19.0 & 8.8 & 2.0 & 8.0 & 2.0 & 9.7 & 1.9 & 2.0 & 18.0 & 13.0 & 12.0 & 11.0 & 4.0 & 3.0 & 9.0 & 9.3 & 8.5  \\ 
# \rowcolor{olive!15} Qwen2.5-Coder &   1.5B &  32.4 & 22.9 & 10.8 & 2.9 & 3.0 & 3.0 & 1.9 & 1.9 & 6.0 & 17.0 & 24.0 & 21.0 & 16.0 & 5.0 & 11.0 & 17.0 & 13.2 & 11.4 \\ 
# \rowcolor{olive!15} Qwen2.5-Coder &   3B  &  35.2 & 24.8 & 11.8 & 2.0 & 11.0 & 5.0 & 11.7 & 1.9 & 0.0 & 18.0 & 26.0 & \underline{29.0} & 22.0 & 12.0 & \underline{15.0} & 23.0 & 16.7 & \underline{14.4}        \\ 
# \rowcolor{olive!15} Granite-Coder &   3B &  25.7 & 21.0 & 10.8 & \underline{4.9} & 7.0 & 3.0 & \underline{12.6} & \underline{3.9} & 6.0 & 14.0 & 18.0 & 11.0 & 15.0 & 1.0 & 5.0 & 12.0 & 12.6 & 8.9 \\ 
# \rowcolor{olive!15} OpenCoder &      1.5B &  \underline{37.1} & 23.8 & 16.7 & 3.9 & \underline{25.0} & 3.0 & 4.9 & 1.9 & 9.0 & 14.0 & 22.0 & 13.0 & 21.0 & 4.0 & 7.0 & 18.0 & \underline{17.9} & 10.2   \\ 
# \rowcolor{olive!15} Yi-Coder &   1.5B &    32.4 & 21.0 & 13.7 & 2.0 & 13.0 & 4.0 & 11.7 & 2.9 & 8.0 & 17.0 & 26.0 & 21.0 & 16.0 & 4.0 & 8.0 & 14.0 & 16.2 & 10.7   \\ 
# \rowcolor{olive!15} Qwen3 & 0.6B & 14.3 & 23.8 & 2.9 & 2.9 & 0.0 & 5.0 & 0.0 & 2.9 & 2.0 & 24.0 & 18.0 & 22.0 & 10.0 & 7.0 & 2.0 & 14.0 & 6.2 & 12.7            \\ 
# \rowcolor{olive!15} Qwen3-think &   0.6B  & 13.3 & 15.2 & 2.0 & 2.0 & 1.0 & 5.0 & 0.0 & 1.9 & 2.0 & 6.0 & 8.0 & 3.0 & 13.0 & 0.0 & 0.0 & 6.0 & 4.9 & 4.9        \\ 
# \rowcolor{olive!15} Qwen3 &   1.7B  & 23.8 & 26.7 & 8.8 & 3.9 & 3.0 & 4.0 & 3.9 & 1.9 & 12.0 & 22.0 & 22.0 & 16.0 & 19.0 & 9.0 & 7.0 & 23.0 & 12.5 & 13.3 \\ 
# \rowcolor{olive!15} Qwen3-think &   1.7B  & 25.7 & 21.0 & 3.9 & 2.9 & 3.0 & 2.0 & 0.0 & 2.9 & 10.0 & 11.0 & 22.0 & 17.0 & \underline{28.0} & 2.0 & 7.0 & 13.0 & 12.5 & 9.0 \\        
# \rowcolor{olive!15} Qwen3 &   4B  & 26.7 & \underline{28.6} & 7.8 & 5.9 & 7.0 & \underline{6.0} & 1.9 & 1.9 & \underline{16.0} & \underline{25.0} & \underline{29.0} & 28.0 & \underline{28.0} & \underline{13.0} & 7.0 & \underline{38.0} & 15.4 & 18 \\ 
# \rowcolor{olive!15} Qwen3-think &   4B  & 34.3 & 21.9 & 12.7 & 4.9 & 6.0 & 4.0 & 1.0 & 3.9 & 12.0 & 12.0 & \underline{29.0} & 20.0 & 25.0 & 2.0 & 13.0 & 17.0 & 16.7 & 10.7   \\ \midrule
# \multicolumn{20}{c}{\textit{6B+ Open-source LLMs}}       \\ \midrule
# \rowcolor{magenta!15}  CodeLlama &   7B &       18.1 & 22.9 & 5.9 & 3.9 & 3.0 & \underline{4.0} & 2.9 & 2.9 & 7.0 & 19.0 & 20.0 & 22.0 & 13.0 & 9.0 & 10.0 & 21.0 & 10.0 & 13.1  \\ 
# \rowcolor{magenta!15}  Llama3.1 &   8B &   40.0 & 16.2 & 8.8 & 0.0 & 13.0 & 3.0 & 10.7 & 1.9 & 12.0 & 20.0 & 27.0 & 19.0 & 26.0 & 7.0 & 7.0 & 18.0 & 18.1 & 10.6        \\ 
# \rowcolor{magenta!15} Deepseek-Coder & 6.7B &    37.1 & 21.9 & \underline{27.5} & \underline{7.8} & 20.0 & 3.0 & 4.9 & 1.9 & 16.0 & 17.0 & 30.0 & 20.0 & 30.0 & 8.0 & 12.0 & 19.0 & 22.2 & 12.3          \\ 
# \rowcolor{magenta!15} Yi-Coder &   9B &  \underline{46.7} & 27.6 & 20.6 & 3.9 & 21.0 & 3.0 & \underline{12.6} & 2.9 & 17.0 & 20.0 & 38.0 & 28.0 & 38.0 & 8.0 & 17.0 & 23.0 & 26.4 & 14.6     \\ 
# \rowcolor{magenta!15} Granite-Coder &   8B &  35.2 & 19.0 & 11.8 & 3.9 & 11.0 & 3.0 & 3.9 & 1.9 & 13.0 & 15.0 & 32.0 & 15.0 & 21.0 & 1.0 & 11.0 & 8.0 & 17.4 & 8.4      \\ 
# \rowcolor{magenta!15} OpenCoder &     8B  &   38.1 & 24.8 & 21.6 & 5.9 & \underline{24.0} & \underline{4.0} & 5.8 & 1.9 & 16.0 & 17.0 & \underline{42.0} & 19.0 & 26.0 & 9.0 & 14.0 & 15.0 & 23.5 & 12.1          \\ 
# \rowcolor{magenta!15} CodeQwen1.5 &   7B &   33.3 & 26.7 & 17.6 & 5.9 & 10.0 & \underline{4.0} & 4.9 & 1.9 & 14.0 & \underline{23.0} & 33.0 & 22.0 & 29.0 & 9.0 & 17.0 & 18.0 & 19.9 & 13.8            \\ 
# \rowcolor{magenta!15} Qwen2.5-Coder &   7B & 41.9 & 27.6 & 25.5 & 3.9 & 16.0 & 3.0 & 11.7 & 2.9 & \underline{19.0} & 22.0 & 36.0 & \underline{30.0} & \underline{43.0} & 11.0 & 20.0 & \underline{28.0} & \underline{26.7} & \underline{16.0}      \\  
# \rowcolor{magenta!15}  Qwen3 &   8B &  35.2 & \underline{33.3} & 13.7 & 7.8 & 12.0 & \underline{4.0} & 8.7 & 4.9 & 0.0 & 0.0 & 30.0 & 26.0 & 30.0 & \underline{19.0} & 9.0 & 27.0 & 17.4 & 15.3  \\ 
# \rowcolor{magenta!15} Qwen3-think &   8B &        35.2 & 31.4 & 15.7 & 9.8 & 6.0 & \underline{4.0} & 1.9 & \underline{5.8} & 16.0 & 14.0 & 30.0 & 24.0 & 28.0 & 2.0 & \underline{22.0} & 14.0 & 19.4 & 13.2        \\ 
#  \midrule
# \multicolumn{20}{c}{\textit{14B+ Open-source LLMs}}      \\ \midrule
# \rowcolor{violet!15} CodeLlama &   13B &  23.8 & 26.7 & 11.8 & 6.9 & 6.0 & \underline{5.0} & 1.0 & \underline{5.8} & 7.0 & 21.0 & 26.0 & 5.0 & 14.0 & 8.0 & 9.0 & 23.0 & 12.3 & 12.7         \\ 
# \rowcolor{violet!15} Qwen2.5-Coder &   14B & 48.6 & 27.6 & \underline{27.5} & 7.8 & \underline{22.0} & 2.0 & \underline{18.4} & 2.9 & 20.0 & \underline{25.0} & 38.0 & 31.0 & 34.0 & 12.0 & 20.0 & 35.0 & 28.6 & 17.9 \\
# \rowcolor{violet!15} Qwen3 &   14B &   36.2 & \underline{33.3} & 25.5 & 8.8 & 20.0 & 3.0 & 8.7 & 3.9 & 23.0 & 22.0 & 37.0 & 31.0 & 36.0 & \underline{20.0} & 18.0 & \underline{53.0} & 25.6 & \underline{21.9}        \\ 
# \rowcolor{violet!15} Qwen3-think &   14B &   \underline{51.4} & 31.4 & 22.5 & \underline{15.7} & 16.0 & \underline{5.0} & 1.9 & 4.9 & \underline{30.0} & 24.0 & \underline{48.0} & \underline{33.0} & \underline{43.0} & 4.0 & \underline{24.0} & 17.0 & \underline{29.6} & 16.9       \\ 
# \rowcolor{violet!15} Granite-Coder &   20B & 33.3 & 17.1 & 15.7 & 3.9 & 5.0 & \underline{5.0} & 4.9 & 1.9 & 15.0 & 15.0 & 26.0 & 19.0 & 22.0 & 4.0 & 11.0 & 9.0 & 16.7 & 9.4         \\ 
# \midrule
# \multicolumn{20}{c}{\textit{32B+ Open-source LLMs \& MoE LLMs}}      \\ \midrule
# \rowcolor{red!15} Granite-Coder &   34B &  37.1 & 21.0 & 16.7 & 2.9 & 13.0 & 4.0 & 5.8 & 1.9 & 11.0 & 15.0 & 24.0 & 16.0 & 24.0 & 3.0 & 10.0 & 3.0 & 17.8 & 8.4        \\ 
# \rowcolor{red!15} CodeLlama &   34B & 16.2 & 21.9 & 9.8 & 4.9 & 5.0 & 3.0 & 8.7 & 2.9 & 8.0 & 9.0 & 23.0 & 2.0 & 16.0 & 6.0 & 9.0 & 17.0 & 12.0 & 8.4        \\ 
# \rowcolor{red!15} Deepseek-Coder & 33B &  41.9 & 22.9 & 33.3 & 4.9 & 22.0 & 4.0 & 7.8 & 1.9 & 24.0 & 20.0 & 33.0 & 18.0 & 37.0 & 7.0 & 19.0 & 20.0 & 27.3 & 12.3       \\ 
# \rowcolor{red!15} Qwen2.5-Coder &    32B &   42.9 & 33.3 & 22.5 & 6.9 & 20.0 & 6.0 & 8.7 & 4.9 & 29.0 & 30.0 & 47.0 & 30.0 & 42.0 & 16.0 & 27.0 & 39.0 & 29.9 & 20.7           \\ 
# \rowcolor{red!15} Llama3.1 &    70B &   42.9 & 33.3 & 22.5 & 6.9 & 20.0 & 6.0 & 8.7 & 4.9 & 29.0 & 30.0 & 47.0 & 30.0 & 42.0 & 16.0 & 27.0 & 39.0 & 29.9 & 20.7           \\ 
# \rowcolor{red!15} Qwen3 & 32B &   49.5 & 33.3 & 25.5 & 8.8 & 17.0 & 7.0 & \underline{10.7} & 1.9 & 20.0 & 29.0 & 38.0 & \underline{34.0} & 41.0 & \underline{28.0} & 22.0 & \underline{52.0} & 28.0 & \underline{24.2}     \\ 
# \rowcolor{red!15} Qwen3-think & 32B &   49.5 & 33.3 & 25.5 & 8.8 & 17.0 & 7.0 & \underline{10.7} & 1.9 & 20.0 & 29.0 & 38.0 & \underline{34.0} & 41.0 & \underline{28.0} & 22.0 & \underline{52.0} & 28.0 & \underline{24.2}     \\ 
# \rowcolor{red!15} Qwen3 & 3/30B &  54.3 & 30.5 & 30.4 & 11.8 & 31.0 & 4.0 & 1.0 & 4.9 & 31.0 & 26.0 & 48.0 & 28.0 & 46.0 & 2.0 & 36.0 & 21.0 & 34.7 & 16.0           \\ 
# \rowcolor{red!15} Qwen3-think & 3/30B & 35.2 & 33.3 & 16.7 & 11.8 & 14.0 & 6.0 & 1.9 & 4.9 & 32.0 & 30.0 & 45.0 & 33.0 & 46.0 & 4.0 & 34.0 & 22.0 & 28.0 & 18.1\\
# \rowcolor{red!15} Qwen3 & 22B/235B &  50.5 & 33.3 & 28.4 & 9.8 & 14.0 & 2.0 & 1.9 & 4.9 & 20.0 & 24.0 & 43.0 & 29.0 & 42.0 & 16.0 & 26.0 & 35.0 & 28.3 & 19.3     \\ 
# \rowcolor{red!15} Qwen3-think & 22B/235B &   48.6 & 32.4 & 21.6 & 10.8 & 20.0 & \underline{12.0} & 2.9 & \underline{6.8} & 21.0 & 15.0 & 37.0 & 22.0 & 47.0 & 4.0 & 35.0 & 15.0 & 29.1 & 14.8        \\ 
# \rowcolor{red!15} Deepseek-V3 & 37/637B & 51.4 & 36.2 & 29.4 & 9.8 & 23.0 & 4.0 & 2.9 & 1.9 & 31.0 & 32.0 & 51.0 & 31.0 & 54.0 & 24.0 & 33.0 & 35.0 & 34.4 & 21.7     \\ 
# \rowcolor{red!15} Deepseek-R1 & 37/637B &    58.1 & 37.1 & 37.3 & 12.7 & 38.0 & 5.0 & 4.9 & 5.8 & 46.0 & 35.0 & 55.0 & 28.0 & 61.0 & 6.0 & 45.0 & 20.0 & 43.1 & 18.8        \\ 
# \rowcolor{red!15} \textbf{\baseline{}} &    32B &   58.3 & 38.2 & 39.3 & 13.5 & 30.0 & 12.0 & 10.7 & 6.8 & 44.0 & 38.0 & 47.0 & 38.0 & 48.0 & 30.0 & 45.0 & 52.0 & 40.3 & 34.2  \\ 
# \bottomrule
# \end{tabular}}
# \vspace{-10pt}
# \label{tab:ifevalcode_en}
# \end{table*}
# """

latex = r"""
\begin{table*}[]
\caption{Chinese evaluation results in \benchmark{} of 8 programming languages. `Corr..' denotes the correctness of the model-generated response, and `Instr.' denotes the instruction-following accuracy of the response. The underlined fonts denote the best performance in the same parameter range.}
\resizebox{1.0\textwidth}{!}{
\begin{tabular}{lc|cccccccccccccccccc}
\toprule
\multirow{2}{*}{Models}  & \multirow{2}{*}{Params} & \multicolumn{2}{c}{Python} & \multicolumn{2}{c}{Java} & \multicolumn{2}{c}{Cpp} & \multicolumn{2}{c}{C-sharp} & \multicolumn{2}{c}{Typescript} & \multicolumn{2}{c}{Javascript} & \multicolumn{2}{c}{Php} & \multicolumn{2}{c}{Shell} & \multicolumn{2}{c}{Avg.} \\ \cmidrule{3-20} 
 &    & Corr.       & Instr.       & Corr.      & Instr.      & Corr.      & Instr.     & Corr.        & Instr.       & Corr.         & Instr.         & Corr.         & Instr.         & Corr.      & Instr.     & Corr.       & Instr.      & Corr.      & Instr.      \\ \midrule
\multicolumn{20}{c}{\textit{Closed-source LLMs}}   \\ \midrule
\rowcolor{cyan!15} Claude-3.5-Sonnet  & \faLock{}   &  49.5 & 33.3 & \underline{38.2} & 11.8 & 23.0 & 7.0 & 14.6 & 2.9 & 20.0 & 29.0 & 45.0 & \underline{32.0} & 47.0 & 29.0 & 27.0 & 36.0 & 33.1 & 22.6\\  
\rowcolor{cyan!15} Claude-3.7-Sonnet  & \faLock{}   &  47.6 & 28.6 & 36.3 & 7.8 & 28.0 & 7.0 & 12.6 & 3.9 & 30.0 & \underline{30.0} & 51.0 & 30.0 & \underline{61.0} & 22.0 & 37.0 & 44.0 & \underline{37.9} & 21.6 \\  
\rowcolor{cyan!15} GPT-4o  & \faLock{}   &   42.9 & 39.0 & 24.5 & 7.8 & 22.0 & 7.0 & 14.6 & 3.9 & 27.0 & 26.0 & 46.0 & 23.0 & 51.0 & 27.0 & 30.0 & 42.0 & 32.2 & 22.0 \\
\rowcolor{cyan!15} GPT-4o-mini  & \faLock{}   &  45.7 & 28.6 & 21.6 & 9.8 & 19.0 & 3.0 & 12.6 & 2.9 & 20.0 & 25.0 & 40.0 & 28.0 & 43.0 & 25.0 & 20.0 & 31.0 & 27.8 & 19.1 \\
\rowcolor{cyan!15} GPT-4.1  & \faLock{}   &  51.4 & 39.0 & 35.3 & 11.8 & 25.0 & 7.0 & 0.0 & 2.9 & \underline{35.0} & 27.0 & 51.0 & 29.0 & 54.0 & 35.0 & 40.0 & 46.0 & 36.4 & \underline{24.7} \\
\rowcolor{cyan!15} GPT-4.1-mini  & \faLock{}   &  46.7 & 36.2 & \underline{38.2} & 6.9 & 18.0 & 3.0 & 0.0 & 2.9 & 32.0 & 28.0 & 50.0 & 28.0 & 46.0 & 33.0 & 43.0 & \underline{52.0} & 34.2 & 23.7 \\
\rowcolor{cyan!15} o1-mini  & \faLock{}   & \underline{58.1} & 32.4 & 30.4 & 12.7 & \underline{29.0} & 9.0 & \underline{17.5} & 2.9 & 34.0 & 25.0 & \underline{55.0} & 28.0 & 53.0 & 31.0 & 37.0 & 47.0 & 39.3 & 23.5 \\
\rowcolor{cyan!15} o3-mini  & \faLock{}   &   54.3 & 37.1 & 34.3 & 12.7 & 25.0 & 7.0 & 15.5 & 3.9 & 32.0 & 25.0 & \underline{55.0} & 29.0 & 51.0 & 31.0 & 35.0 & 47.0 & 37.8 & 24.1 \\
\rowcolor{cyan!15} o4-mini  & \faLock{}   & 53.3 & \underline{40.0} & 29.4 & \underline{21.6} & 35.0 & 12.0 & \underline{7.8} & 7.8 & 19.0 & 1.0 & 35.0 & 0.0 & 53.0 & \underline{42.0} & \underline{44.0} & 49.0 & 34.6 & 21.7 \\
\rowcolor{cyan!15} grok-3  & \faLock{}   &  30.5 & 24.8 & 24.5 & 9.8 & 2.0 & 5.0 & 0.0 & 2.9 & 4.0 & 16.0 & 46.0 & 23.0 & 37.0 & 32.0 & 16.0 & 35.0 & 20.0 & 18.5 \\
\rowcolor{cyan!15} grok-3-mini-fast  & \faLock{}   & 34.3 & 32.4 & 11.8 & 5.9 & 13.0 & \underline{13.0} & 1.9 & 2.9 & 26.0 & 21.0 & 44.0 & 27.0 & 33.0 & 4.0 & 12.0 & 20.0 & 22.0 & 15.8 \\
\midrule


\multicolumn{20}{c}{\textit{0.5B+ Open-source LLMs}}     \\ \midrule
\rowcolor{olive!15} Deepseek-Coder & 1.3B &   22.9 & 10.5 & 14.7 & 1.0 & 7.0 & 2.0 & 1.9 & 1.9 & 0.0 & 1.0 & 16.0 & 13.0 & 7.0 & 7.0 & 1.0 & 2.0 & 8.9 & 4.8         \\ 
\rowcolor{olive!15} Qwen2.5-Coder &   0.5B &  15.2 & 16.2 & 10.8 & 2.0 & 8.0 & 3.0 & 7.8 & 1.9 & 1.0 & 14.0 & 13.0 & 15.0 & 7.0 & 7.0 & 1.0 & 11.0 & 8.0 & 8.8  \\ 
\rowcolor{olive!15} Qwen2.5-Coder &   1.5B &  28.6 & 21.9 & 9.8 & 2.9 & 2.0 & 5.0 & 0.0 & 1.9 & 6.0 & 20.0 & 28.0 & \underline{23.0} & 18.0 & 11.0 & 4.0 & 24.0 & 12.1 & 13.7 \\ 
\rowcolor{olive!15} Qwen2.5-Coder &   3B  & 31.4 & 20.0 & 13.7 & 3.9 & 12.0 & 5.0 & 11.7 & 2.9 & 7.0 & 19.0 & \underline{31.0} & \underline{23.0} & 27.0 & 12.0 & 10.0 & 30.0 & \underline{18.0} & 14.4      \\ 
\rowcolor{olive!15} Granite-Coder &   3B &  25.7 & 21.0 & 10.8 & 4.9 & 7.0 & 3.0 & 12.6 & \underline{3.9} & 6.0 & 14.0 & 18.0 & 11.0 & 15.0 & 1.0 & 5.0 & 12.0 & 12.6 & 8.9 \\ 
\rowcolor{olive!15} OpenCoder & 1.5B & \underline{39.0} & 16.2 & \underline{21.6} & 3.9 & \underline{20.0} & 2.0 & 6.8 & 1.9 & 10.0 & 14.0 & 18.0 & 14.0 & 21.0 & 8.0 & 7.0 & 17.0 & \underline{18.0} & 9.6   \\ 
\rowcolor{olive!15} Yi-Coder &   1.5B &  34.3 & 17.1 & 15.7 & 1.0 & 16.0 & 5.0 & \underline{14.6} & 1.9 & 10.0 & 11.0 & 22.0 & 21.0 & 15.0 & 7.0 & 2.0 & 13.0 & 16.3 & 9.6   \\ 
\rowcolor{olive!15} Qwen3 & 0.6B & 11.4 & 21.0 & 2.9 & 3.9 & 1.0 & \underline{6.0} & 0.0 & 1.9 & 0.0 & 25.0 & 13.0 & 19.0 & 8.0 & 15.0 & 0.0 & 22.0 & 4.6 & 14.2    \\ 
\rowcolor{olive!15} Qwen3-think & 0.6B & 10.5 & 10.5 & 2.9 & 3.9 & 0.0 & 2.0 & 0.0 & 1.9 & 1.0 & 10.0 & 9.0 & 8.0 & 6.0 & 1.0 & 0.0 & 7.0 & 3.7 & 5.6  \\ 
\rowcolor{olive!15} Qwen3 &   1.7B  & 27.6 & \underline{29.5} & 6.9 & 3.9 & 4.0 & 5.0 & 1.0 & 1.9 & 9.0 & 25.0 & 19.0 & 19.0 & 15.0 & 13.0 & 5.0 & 31.0 & 11.0 & 16.0 \\ 
\rowcolor{olive!15} Qwen3-think &   1.7B  & 21.0 & 14.3 & 2.9 & 2.9 & 0.0 & 0.0 & 0.0 & 1.0 & 10.0 & 1.0 & 14.0 & 3.0 & 21.0 & 2.0 & 3.0 & 3.0 & 9.0 & 3.5  \\        
\rowcolor{olive!15} Qwen3 &   4B  & 24.8 & 30.5 & 6.9 & \underline{7.8} & 5.0 & 4.0 & 2.9 & \underline{3.9} & \underline{14.0} & \underline{26.0} & 28.0 & 31.0 & \underline{29.0} & \underline{20.0} & 8.0 & \underline{47.0} & 14.8 & \underline{21.2} \\ 
\rowcolor{olive!15} Qwen3-think &   4B  & 24.8 & 7.6 & 4.9 & 1.0 & 1.0 & 1.0 & 0.0 & 0.0 & 9.0 & 5.0 & 16.0 & 3.0 & 21.0 & 1.0 & \underline{14.0} & 6.0 & 11.4 & 3.1  \\ \midrule


\multicolumn{20}{c}{\textit{6B+ Open-source LLMs}}       \\ \midrule
\rowcolor{magenta!15}  CodeLlama &   7B &    0.0 & 1.9 & 5.9 & 1.0 & 1.0 & 3.0 & 0.0 & 2.9 & 5.0 & 2.0 & 23.0 & 0.0 & 1.0 & 2.0 & 2.0 & 17.0 & 4.7 & 3.7  \\ 
\rowcolor{magenta!15}  Llama3.1 &   8B &  35.2 & 21.9 & 9.8 & 2.0 & 13.0 & 2.0 & \underline{15.5} & 1.9 & 10.0 & 19.0 & 24.0 & 23.0 & 24.0 & 14.0 & 5.0 & 24.0 & 17.2 & 13.5      \\ 
\rowcolor{magenta!15} Deepseek-Coder & 6.7B &   38.1 & 23.8 & 20.6 & 3.9 & 16.0 & 3.0 & 2.9 & 1.9 & \underline{18.0} & 16.0 & 34.0 & 17.0 & 25.0 & 10.0 & 16.0 & 23.0 & 21.4 & 12.3        \\ 
\rowcolor{magenta!15} Yi-Coder &   9B & \underline{43.8} & 24.8 & \underline{31.4} & \underline{5.9} & \underline{21.0} & 2.0 & 7.8 & 1.9 & \underline{18.0} & 16.0 & 33.0 & 24.0 & \underline{46.0} & 11.0 & 14.0 & 23.0 & \underline{26.9} & 13.6  \\ 
\rowcolor{magenta!15} Granite-Coder &   8B & 32.4 & 19.0 & 11.8 & 3.9 & 14.0 & 4.0 & 6.8 & 1.9 & 9.0 & 13.0 & 29.0 & 19.0 & 9.0 & 3.0 & 10.0 & 16.0 & 15.3 & 10.0   \\ 
\rowcolor{magenta!15} OpenCoder &     8B  &   40.0 & 25.7 & 17.6 & 4.9 & 16.0 & \underline{5.0} & 4.9 & 1.9 & 15.0 & 19.0 & 30.0 & 19.0 & 32.0 & 12.0 & 13.0 & 26.0 & 21.1 & 14.2         \\ 
\rowcolor{magenta!15} CodeQwen1.5 &   7B &  41.0 & 21.9 & 15.7 & 4.9 & 12.0 & 4.0 & 9.7 & 1.9 & 12.0 & \underline{23.0} & 33.0 & 25.0 & 27.0 & 11.0 & 13.0 & 23.0 & 20.5 & 14.3        \\ 
\rowcolor{magenta!15} Qwen2.5-Coder &   7B & 42.9 & 27.6 & 21.6 & 4.9 & 11.0 & \underline{5.0} & 6.8 & 2.9 & 16.0 & 21.0 & \underline{39.0} & 29.0 & 36.0 & 11.0 & \underline{21.0} & \underline{32.0} & 24.3 & \underline{16.7}     \\  
\rowcolor{magenta!15}  Qwen3 &   8B &  36.2 & \underline{32.4} & 11.8 & \underline{5.9} & 7.0 & \underline{5.0} & 5.8 & \underline{3.9} & 0.0 & 0.0 & 29.0 & 32.0 & \underline{32.0} & \underline{27.0} & 6.0 & 18.0 & 16.0 & 15.6 \\ 
\rowcolor{magenta!15} Qwen3-think &   8B &  28.6 & 12.4 & 8.8 & 2.9 & 3.0 & 1.0 & 1.9 & 1.0 & 14.0 & 2.0 & 26.0 & 6.0 & 27.0 & 0.0 & 15.0 & 6.0 & 15.6 & 4.0       \\ 
 \midrule


 
\multicolumn{20}{c}{\textit{14B+ Open-source LLMs}}      \\ \midrule
\rowcolor{violet!15} CodeLlama &   13B &  19.0 & 22.9 & 10.8 & 3.9 & 7.0 & \underline{4.0} & 4.9 & 2.9 & 7.0 & 24.0 & 24.0 & 8.0 & 22.0 & 7.0 & 4.0 & 22.0 & 12.3 & 11.9        \\ 
\rowcolor{violet!15} Qwen2.5-Coder &   14B &47.6 & 29.5 & \underline{26.5} & \underline{8.8} & \underline{22.0} & 3.0 & \underline{19.4} & 2.9 & \underline{24.0} & \underline{32.0} & \underline{41.0} & 30.0 & 39.0 & 15.0 & 19.0 & 36.0 & \underline{29.9} & 19.6\\
\rowcolor{violet!15} Qwen3 &   14B &  39.0 & \underline{32.4} & 19.6 & \underline{8.8} & 17.0 & 3.0 & 10.7 & \underline{4.9} & 23.0 & 31.0 & \underline{41.0} & \underline{33.0} & \underline{40.0} & \underline{23.0} & 18.0 & \underline{53.0} & 26.0 & \underline{23.6}    \\ 
\rowcolor{violet!15} Qwen3-think &   14B &  \underline{49.5} & 26.7 & 16.7 & 2.9 & 10.0 & 1.0 & 2.9 & 1.0 & 23.0 & 8.0 & 34.0 & 6.0 & 37.0 & 1.0 & \underline{22.0} & 10.0 & 24.4 & 7.2    \\ 
\rowcolor{violet!15} Granite-Coder &   20B & 30.5 & 21.9 & 15.7 & 2.9 & 4.0 & 4.0 & 6.8 & 3.9 & 13.0 & 13.0 & 25.0 & 19.0 & 26.0 & 3.0 & 4.0 & 10.0 & 15.7 & 9.8      \\ 
\midrule
\multicolumn{20}{c}{\textit{32B+ Open-source LLMs \& MoE LLMs}}      \\ \midrule
\rowcolor{red!15} Granite-Coder &   34B & 34.3 & 23.8 & 12.7 & 4.9 & 10.0 & 4.0 & 5.8 & 1.9 & 16.0 & 15.0 & 29.0 & 23.0 & 24.0 & 4.0 & 5.0 & 9.0 & 17.2 & 10.7   \\ 
\rowcolor{red!15} CodeLlama &  34B & 4.8 & 15.2 & 5.9 & 2.0 & 15.0 & 3.0 & 12.6 & 1.9 & 10.0 & 6.0 & 18.0 & 0.0 & 17.0 & 10.0 & 3.0 & 22.0 & 10.7 & 7.5       \\ 
\rowcolor{red!15} Deepseek-Coder & 33B &  44.8 & 21.0 & 26.5 & 4.9 & 24.0 & \underline{7.0} & 7.8 & 1.9 & 21.0 & 18.0 & 35.0 & 20.0 & 30.0 & 14.0 & 20.0 & 26.0 & 26.2 & 14.1    \\ 
\rowcolor{red!15} Qwen2.5-Coder &    32B &  43.8 & 34.3 & 28.4 & 8.8 & 19.0 & 2.0 & \underline{12.6} & 5.8 & 25.0 & 29.0 & 41.0 & 34.0 & 44.0 & 24.0 & 23.0 & 38.0 & 29.6 & 22.0      \\ 
\rowcolor{red!15} Llama3.1 &    70B &   47.6 & 22.9 & 14.7 & 2.0 & 19.0 & 3.0 & 11.7 & 2.9 & 19.0 & 24.0 & 35.0 & 28.0 & 39.0 & 19.0 & 21.0 & 40.0 & 25.9 & 17.7      \\ 
\rowcolor{red!15} Qwen3 & 32B &  42.9 & \underline{41.0} & 24.5 & 7.8 & 17.0 & \underline{7.0} & 9.7 & 3.9 & 27.0 & 25.0 & 38.0 & 31.0 & 40.0 & 23.0 & 19.0 & 51.0 & 27.3 & 23.7   \\ 
\rowcolor{red!15} Qwen3-think & 32B &  54.3 & 19.0 & 30.4 & 5.9 & 24.0 & 2.0 & 7.8 & 1.9 & 26.0 & 2.0 & 42.0 & 7.0 & 50.0 & 1.0 & 30.0 & 6.0 & 33.1 & 5.7  \\ 
\rowcolor{red!15} Qwen3 & 3/30B & 43.8 & 33.3 & 28.4 & 11.8 & 19.0 & 6.0 & 5.8 & 5.8 & 24.0 & 31.0 & 42.0 & 31.0 & 38.0 & 29.0 & 21.0 & 48.0 & 27.8 & 24.4    \\ 
\rowcolor{red!15} Qwen3-think & 3/30B & 42.9 & 21.0 & 16.7 & 2.9 & 12.0 & 0.0 & 2.9 & 2.9 & 21.0 & 4.0 & 41.0 & 10.0 & 40.0 & 1.0 & 22.0 & 7.0 & 24.8 & 6.2 \\
\rowcolor{red!15} Qwen3 & 22B/235B & 46.7 & 38.1 & 22.5 & 8.8 & 12.0 & 3.0 & 1.0 & 2.9 & 25.0 & 24.0 & 44.0 & 30.0 & 47.0 & 22.0 & 20.0 & 38.0 & 27.3 & 20.9   \\ 
\rowcolor{red!15} Qwen3-think & 22B/235B &   46.7 & 11.4 & 26.5 & 2.0 & 26.0 & 1.0 & 1.0 & 0.0 & 32.0 & 1.0 & 43.0 & 2.0 & 43.0 & 1.0 & 36.0 & 2.0 & 31.7 & 2.6    \\ 
\rowcolor{red!15} Deepseek-V3 & 37/671B & 50.5 & 35.2 & 32.4 & 9.8 & 21.0 & 5.0 & 4.9 & 1.9 & 32.0 & 34.0 & 51.0 & 25.0 & 51.0 & 29.0 & 34.0 & 38.0 & 34.6 & 22.2     \\ 
\rowcolor{red!15} Deepseek-R1 & 37/671B &    \underline{58.1} & 37.1 & 37.3 & 12.7 & \underline{38.0} & 5.0 & 4.9 & 5.8 & 46.0 & \underline{35.0} & \underline{55.0} & 28.0 & \underline{61.0} & 6.0 & 45.0 & 20.0 & \underline{43.1} & 18.8        \\ 
\rowcolor{red!15} \textbf{\baseline{}} &    32B &   54.8 & 39.2 & \underline{40.3} & \underline{13.8} & 34.0 & \underline{7.0} & 11.7 & \underline{6.8} & \underline{48.0} & \underline{35.0} & 49.0 & \underline{40.0} & 48.0 & \underline{32.0} & \underline{51.0} & \underline{55.0} & 42.1 & \underline{28.6}  \\ 
\bottomrule
\end{tabular}}
\label{tab:ifevalcode_zh}
\end{table*}
"""


import re
import json
import time

# latex = r"""
# % （这里省略你的完整 LaTeX 表格内容，保持和之前一致）
# """

# 1. 提取 tabular 环境中的内容
m = re.search(r"\\begin\{tabular\}.*?\\toprule(.*?)\\bottomrule", latex, re.S)
if not m:
    raise ValueError("未能提取到表格主体")
body = m.group(1).splitlines()

def clean_cell(cell: str) -> str:
    """
    去掉 LaTeX 包装命令，并提取纯文本数字或字符串
    """
    # 去掉 \rowcolor{}, \faLock{}, % 等
    cell = re.sub(r"\\rowcolor\{.*?\}", "", cell)
    cell = cell.replace("\\faLock{}", "🔒")
    # 去掉 \underline{}、\textbf{} 包装
    cell = re.sub(r"\\underline\{(.*?)\}", r"\1", cell)
    cell = re.sub(r"\\textbf\{(.*?)\}", r"\1", cell)
    # 去掉可能残留的花括号
    cell = cell.replace("{", "").replace("}", "")
    return cell.strip()

def parse_number(s: str):
    """
    从字符串中抽取第一个类似浮点数的子串并转成 float
    """
    m = re.search(r"[-+]?\d*\.\d+|\d+", s)
    return float(m.group()) if m else None

performances = []
models = []

for line in body:
    line = line.strip()
    # 跳过注释、空行和命令行
    if not line or line.startswith("%"):
        continue
    if any(tok in line for tok in ["\\midrule", "\\cmidrule", "\\multicolumn", "\\multirow"]):
        continue

    # 去掉行尾的 \\
    line = re.sub(r"\\\\\s*$", "", line)
    cols = [clean_cell(c) for c in line.split("&")]

    if len(cols) != 20:
        print(f"跳过（列数 {len(cols)} != 20）: {cols}")
        continue

    perf = {
        "model": cols[0],
        "Params": cols[1],
    }
    langs = ["Python", "Java", "Cpp", "C-sharp", "Typescript", "Javascript", "Php", "Shell"]
    idx = 2
    for lg in langs:
        corr = parse_number(cols[idx])
        inst = parse_number(cols[idx + 1])
        perf[f"{lg} Corr."] = corr
        perf[f"{lg} Inst."] = inst
        idx += 2
    # 平均值
    perf["Avg Corr."] = parse_number(cols[idx])
    perf["Avg Inst."] = parse_number(cols[idx + 1])

    performances.append(perf)
    models.append({"model_name": cols[0]})

# 当前时间戳（毫秒）
ts = int(time.time() * 1000)

output = {
    "performances": performances,
    "models": models,
    "date_marks": [ts]
}

# print(json.dumps(output, indent=4, ensure_ascii=False))

with open("json.json", "w") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)