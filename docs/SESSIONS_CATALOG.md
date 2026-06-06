# Session 8 — Sessions Catalog

Auto-generated catalog of all persisted runs under `S8SharedCode/code/state/sessions/`.

**Total sessions:** 49

---

## Key assignment sessions

### s8-7f8a75bf — Part 1 / hello

**Query:** Say hello.

**Skills:** planner, formatter

**Nodes:** 2 | **Shape:** planner

**Final answer:**

> Hello!

---

### s8-5c7b354b — Part 1 / A (Shannon)

**Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.

**Skills:** planner, researcher, distiller, formatter

**Nodes:** 4 | **Shape:** planner

**Final answer:**

> Claude Shannon was born on April 30, 1916, and passed away on February 24, 2001. His three key contributions to information theory are:
> 
> 1. The introduction of information entropy as a measure of uncertainty.
> 2. The development of the concept of 'bits' as the fundamental unit of information.
> 3. The definition of channel capacity, which is the maximum rate of reliable information transmission over a noisy channel.

---

### s8-30cc4b2c — Part 1 / I + Part 4 coder

**Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.

**Skills:** planner, researcher, coder, formatter, sandbox_executor

**Nodes:** 7 | **Shape:** planner

**Final answer:**

> The populations of the cities are:
> * London: 9,000,000
> * Paris: 2,141,000
> * Berlin: 3,645,000
> 
> The two cities closest in population are Paris and Berlin.

---

### s8-ea8e55ff — Part 1 / J

**Query:** Read /nonexistent/path.txt and tell me what's in it.

**Skills:** planner, formatter

**Nodes:** 2 | **Shape:** planner

**Final answer:**

> I am sorry, but I was unable to read the file at /nonexistent/path.txt. It is possible that the file does not exist or I do not have the necessary permissions to access it.

---

### s8-65c8069d — Part 1 / K (interrupt)

**Query:** For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest.

**Skills:** planner, researcher, formatter

**Nodes:** 5 | **Shape:** planner

**Final answer:**

> I am sorry, but I was unable to find the current populations and growth rates for Lagos, Cairo, and Kinshasa. Therefore, I cannot determine which city is growing fastest.

---

### s8-453bce58 — Part 2 / parallel fan-out

**Query:** Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CRISPR — one sentence on what CRISPR is. (2) From https://en.wikipedia.org/wiki/MRNA_vaccine — one sentence on how mRNA vaccines work. (3) From https://en.wikipedia.org/wiki/Photovoltaic_effect — one sentence on how solar cells convert light. Then merge the three answers and say which two topics are most related to medicine.

**Skills:** planner, researcher, summariser, comparator, formatter

**Nodes:** 9 | **Shape:** planner

**Final answer:**

> CRISPR is a technology that allows scientists to edit DNA. mRNA vaccines work by instructing cells to produce a specific protein, triggering an immune response. Solar cells convert light energy into electrical energy. Of these three topics, CRISPR and mRNA vaccines are most related to medicine.

---

### s8-14af4aa5 — Part 2 / alternate (4 cities)

**Query:** Find the 2025 populations of Tokyo, Delhi, Shanghai, and Sao Paulo, then tell me which two are closest in size.

**Skills:** planner, researcher, distiller, formatter

**Nodes:** 7 | **Shape:** planner

**Final answer:**

> I am sorry, but I could not find the 2025 populations for Tokyo, Delhi, Shanghai, and Sao Paulo, nor could I determine which two are closest in size based on the information I have.

---

### s8-4fd467a0 — Part 3 / critic pass

**Query:** Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers.

**Skills:** planner, coder, critic, formatter, sandbox_executor

**Nodes:** 5 | **Shape:** planner

**Final answer:**

> The sum of 23 and 19 is 42.

---

### s8-418393c0 — Part 3 / critic fail + recovery

**Query:** Use Python to compute 23 plus 19. The coder must first emit JSON {"sum": 99}. Use an explicit critic that fails when sum does not equal 23+19. On critic failure, recovery must replan so the coder emits the correct sum and the critic passes before formatting.

**Skills:** planner, coder, critic, formatter, sandbox_executor

**Nodes:** 13 | **Shape:** planner

**Final answer:**

> {"exit_code": 0, "stdout": "{\"sum\": 42}\n", "stdout_truncated": false, "stderr": "", "stderr_truncated": false, "files_written": [], "timed_out": false, "cwd": "/tmp/s8sandbox-y497qfh8"}

---

### s8-a6972d7c — Part 5 / comparator

**Query:** Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size.

**Skills:** planner, researcher, coder, comparator, formatter, sandbox_executor

**Nodes:** 14 | **Shape:** planner

**Final answer:**

> I could not find the populations for Madrid and Rome. The population for Lisbon is 505,526. Without the populations for Madrid and Rome, I cannot compare them or determine which two cities are closest in size.

---

### s8-1dc4d047 — Part 5 / comparator (first run)

**Query:** Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size.

**Skills:** planner, researcher, comparator, formatter

**Nodes:** 6 | **Shape:** planner

**Final answer:**

> I am sorry, but I could not find the populations for Madrid, Rome, and Lisbon. Therefore, I am unable to compare them or determine which two are closest in size.

---

## All sessions (newest first)

| Session | Tag | Nodes | Skills | Query (short) |
|---------|-----|-------|--------|---------------|
| s8-d682803b | - | 6 | planner, researcher, coder, comparator,... | Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me whi... |
| s8-899f322e | - | 6 | planner, researcher, coder, comparator,... | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-f0ca5deb | - | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic... |
| s8-802aef8f | - | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. ... |
| s8-75b486ac | - | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic... |
| s8-32965cc9 | - | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. ... |
| s8-3ebef593 | - | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. ... |
| s8-238483a9 | - | 15 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. Emit JSON {"sum": <integer>}. Use an explicit... |
| s8-589d6a69 | - | 15 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic... |
| s8-418393c0 | Part 3 / critic fail + recovery | 13 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. The coder must first emit JSON {"sum": 99}. U... |
| s8-4fd467a0 | Part 3 / critic pass | 5 | planner, coder, critic, formatter, sand... | Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. ... |
| s8-bfe65dca | - | 76 | planner, researcher, distiller, critic,... | Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract three mandatory di... |
| s8-f6312d87 | - | 5 | planner, researcher, distiller, critic,... | Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract birth_year and dea... |
| s8-98739603 | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract birth_year and dea... |
| s8-453bce58 | Part 2 / parallel fan-out | 9 | planner, researcher, summariser, compar... | Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CR... |
| s8-a6972d7c | Part 5 / comparator | 14 | planner, researcher, coder, comparator,... | Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me whi... |
| s8-5c7b354b | Part 1 / A (Shannon) | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-c2958cea | - | 7 | planner, researcher, coder, formatter, ... | For Lagos, Cairo, and Kinshasa, find current populations and growth rates and t... |
| s8-66673ade | - | 7 | planner, researcher, coder, formatter, ... | For Lagos, Cairo, and Kinshasa, find current populations and growth rates and t... |
| s8-ff22fc29 | - | 7 | planner, researcher, coder, formatter, ... | For Lagos, Cairo, and Kinshasa, find current populations and growth rates and t... |
| s8-75238330 | - | 7 | planner, researcher, coder, formatter, ... | For Lagos, Cairo, and Kinshasa, find current populations and growth rates and t... |
| s8-b0fde28e | - | 2 | planner, formatter | Read /nonexistent/path.txt and tell me what's in it. |
| s8-58373bf3 | - | 13 | planner, researcher, coder, formatter, ... | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-e63b0726 | - | 3 | planner, retriever, formatter | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-b7416b3b | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-f4bb5634 | - | 3 | planner, retriever, formatter | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-27746d63 | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-04675211 | - | 2 | planner, formatter | Say hello. |
| s8-6bf10f2e | - | 2 | planner, formatter | Say hello. |
| s8-f3e362d0 | - | 2 | planner, formatter | Say hello in one short sentence. |
| s8-1dc4d047 | Part 5 / comparator (first run) | 6 | planner, researcher, comparator, format... | Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me whi... |
| s8-e3672999 | - | 17 | planner, coder, critic, formatter, sand... | Return a valid JSON object with exactly one key named greeting and value hello,... |
| s8-2cd1b07f | - | 5 | planner, coder, critic, formatter, sand... | Return a valid JSON object with exactly one key named greeting and value hello,... |
| s8-fc3a1651 | - | 5 | planner, coder, critic, formatter, sand... | Return a valid JSON object with exactly one key named greeting and value hello. |
| s8-25b67fc2 | - | 2 | planner, formatter | Respond with exactly 5 characters: Hello |
| s8-14af4aa5 | Part 2 / alternate (4 cities) | 7 | planner, researcher, distiller, formatt... | Find the 2025 populations of Tokyo, Delhi, Shanghai, and Sao Paulo, then tell m... |
| s8-dc7d6377 | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-7cec30bd | - | 4 | planner, retriever, distiller, formatter | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-9706977c | - | 4 | planner, retriever, distiller, formatter | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-30cc4b2c | Part 1 / I + Part 4 coder | 7 | planner, researcher, coder, formatter, ... | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-102c058f | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-65c8069d | Part 1 / K (interrupt) | 5 | planner, researcher, formatter | For Lagos, Cairo, and Kinshasa, find current populations and growth rates and t... |
| s8-ea8e55ff | Part 1 / J | 2 | planner, formatter | Read /nonexistent/path.txt and tell me what's in it. |
| s8-5ae42e16 | - | 5 | planner, retriever, coder, formatter, s... | Find the populations of London, Paris, Berlin and tell me which two are closest... |
| s8-d983be7d | - | 4 | planner, researcher, distiller, formatt... | Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, ... |
| s8-7f8a75bf | Part 1 / hello | 2 | planner, formatter | Say hello. |
| s8-67888488 | - | 1 | planner | Find populations of London, Paris, and Berlin, then use Python to compute which... |
| s8-b2389077 | - | 7 | planner, formatter, retriever, distille... | Say hello. |
| s8-2d10cbcd | - | 1 | planner | Say hello. |

---

## Appendix — DAG shape and final answer (truncated)

### s8-d682803b

- **Query:** Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size.
- **Shape:** planner
- **Final:** The populations of Madrid, Rome, and Lisbon are as follows: * Madrid: 3,300,000 * Rome: 2,800,000 * Lisbon: 550,000 Madrid and Rome are the closest in size, with a difference of 500,000 people.

### s8-899f322e

- **Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.
- **Shape:** planner
- **Final:** The population of Paris is 11.35 million and the population of London is 9.84 million. The population of Berlin is not available. Paris and London are the two closest in size, with a difference of 1.51 million.

### s8-f0ca5deb

- **Query:** Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic that fails when sum is not 42. After critic-fail recovery, do not emit 99 again; formatter must state the correct sum.
- **Shape:** planner
- **Final:** The sum of 23 plus 19 is 42.

### s8-802aef8f

- **Query:** Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers.
- **Shape:** planner
- **Final:** The sum of 23 and 19 is 42.

### s8-75b486ac

- **Query:** Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic that fails when sum is not 42. After critic-fail recovery, do not emit 99 again; formatter must state the correct sum.
- **Shape:** planner
- **Final:** The sum of 23 plus 19 is 42.

### s8-32965cc9

- **Query:** Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers.
- **Shape:** planner
- **Final:** The sum of 23 plus 19 is 42.

### s8-3ebef593

- **Query:** Use Python to compute 23 plus 19. The coder must emit JSON {"sum": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers.
- **Shape:** planner
- **Final:** The sum of 23 plus 19 is 42.

### s8-238483a9

- **Query:** Use Python to compute 23 plus 19. Emit JSON {"sum": <integer>}. Use an explicit critic that must verify sum equals 50 before formatting.
- **Shape:** planner
- **Final:** The critic has indicated that the sum of 23 plus 19 does not equal 50. Therefore, the requested operation cannot be completed as specified.

### s8-589d6a69

- **Query:** Use Python to compute 23 plus 19. Emit JSON {"sum": 99}. Use an explicit critic to verify sum equals 23+19 before formatting.
- **Shape:** planner
- **Final:** {"exit_code": 0, "stdout": "Critic failed: Computed sum (99) does not equal expected sum (42).\n{\"sum\": 99}\n", "stdout_truncated": false, "stderr": "", "stderr_truncated": false, "files_written": [], "timed_out": false, "cwd": "/tmp/s8sandbox-3op...

### s8-bfe65dca

- **Query:** Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract three mandatory distiller fields: birth_year, death_year, and fields_medal_year. All three keys must appear in fields. Use an explicit critic to verify every field is supported by the fetched page. The critic must fail if fields_medal_yea...
- **Shape:** planner
- **Final:** {"verdict": "fail", "rationale": "The 'fields_medal_year' field is missing from the output, despite being a mandatory field, and the Wikipedia page does not contain evidence for a Fields Medal year for Ada Lovelace."}

### s8-f6312d87

- **Query:** Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract birth_year and death_year into distiller fields. Each value must be directly supported by the fetched page text — do not add any other fields. Use an explicit critic node to verify both fields are supported by the researcher output before...
- **Shape:** planner
- **Final:** I am sorry, but I cannot fulfill this request. The provided inputs do not contain the birth year and death year for Ada Lovelace. The critic node's output indicates that the requested fields were not found in the researcher's output.

### s8-98739603

- **Query:** Fetch https://en.wikipedia.org/wiki/Ada_Lovelace and extract birth_year and death_year into distiller fields. Each value must be directly supported by the fetched page text — do not add any other fields.
- **Shape:** planner
- **Final:** Ada Lovelace was born in 1815 and died in 1852.

### s8-c2958cea

- **Query:** For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest.
- **Shape:** planner
- **Final:** Here are the population and growth rate details for Lagos, Cairo, and Kinshasa: * **Cairo**: Population = 9,800,000, Growth Rate = 1.07% * **Kinshasa**: Population = 16,900,000, Growth Rate = N/A. Notes: Growth rate for Kinshasa is not explicitly st...

### s8-66673ade

- **Query:** For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest.
- **Shape:** planner
- **Final:** Here are the current populations and growth rates for Lagos, Cairo, and Kinshasa: * **Lagos:** Population = 21,000,000, Growth Rate = 3.85% * **Cairo:** Population = 20,400,000, Growth Rate = 2.20% * **Kinshasa:** Population = 15,000,000, Growth Rat...

### s8-ff22fc29

- **Query:** For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest.
- **Shape:** planner
- **Final:** I could not find the population or growth rate for Cairo or Kinshasa. For Lagos, the metro area population in 2026 is projected to be 17,804,000 with a growth rate of 3.78%.

### s8-75238330

- **Query:** For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest.
- **Shape:** planner
- **Final:** I am sorry, but I could not retrieve the current population and growth rate data for Lagos, Cairo, and Kinshasa. Therefore, I cannot tell you which city is growing fastest.

### s8-b0fde28e

- **Query:** Read /nonexistent/path.txt and tell me what's in it.
- **Shape:** planner
- **Final:** I am sorry, but I was unable to read the file at /nonexistent/path.txt. It appears the file does not exist or I do not have permission to access it.

### s8-58373bf3

- **Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.
- **Shape:** planner
- **Final:** The populations of the requested cities are: * London: 8,982,000 * Paris: 2,141,000 * Berlin: 3,645,000 The two cities closest in population size are Berlin and London, with a difference of 5,337,000.

### s8-e63b0726

- **Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.
- **Shape:** planner
- **Final:** I cannot find the populations of London, Paris, and Berlin. The knowledge base contains queries about these cities but no specific population figures or comparisons.

### s8-b7416b3b

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** Claude Shannon was born on April 30, 1916, and passed away on February 24, 2001. His three key contributions to information theory are: 1. **The Mathematical Theory of Communication:** This work introduced the concept of information entropy and esta...

### s8-f4bb5634

- **Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.
- **Shape:** planner
- **Final:** I cannot provide the populations of London, Paris, and Berlin as this information is not available in the provided inputs. The inputs indicate that this query has been processed before, but the actual population data is missing.

### s8-27746d63

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** I am sorry, but I could not retrieve Claude Shannon's birth date, death date, or his key contributions to information theory from the provided inputs.

### s8-04675211

- **Query:** Say hello.
- **Shape:** planner
- **Final:** Hello!

### s8-6bf10f2e

- **Query:** Say hello.
- **Shape:** planner
- **Final:** Hello!

### s8-f3e362d0

- **Query:** Say hello in one short sentence.
- **Shape:** planner
- **Final:** Hello!

### s8-e3672999

- **Query:** Return a valid JSON object with exactly one key named greeting and value hello, and also include a second key named note.
- **Shape:** planner
- **Final:** ```json { "greeting": "hello", "note": null } ```

### s8-2cd1b07f

- **Query:** Return a valid JSON object with exactly one key named greeting and value hello, and also include a second key named note.
- **Shape:** planner
- **Final:** I am sorry, but I cannot fulfill this request. The provided inputs do not contain the necessary information to construct the requested JSON object with both a 'greeting' and a 'note' key.

### s8-fc3a1651

- **Query:** Return a valid JSON object with exactly one key named greeting and value hello.
- **Shape:** planner
- **Final:** { "greeting": "hello" }

### s8-25b67fc2

- **Query:** Respond with exactly 5 characters: Hello
- **Shape:** planner
- **Final:** Hello

### s8-dc7d6377

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** I was unable to find Claude Shannon's birth date, death date, or contributions to information theory.

### s8-7cec30bd

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** I was unable to find Claude Shannon's birth date, death date, or any contributions to information theory.

### s8-9706977c

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** I was unable to find Claude Shannon's birth date, death date, or any key contributions to information theory.

### s8-102c058f

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** I am sorry, but I was unable to find Claude Shannon's birth date, death date, or any contributions to information theory from the provided source.

### s8-5ae42e16

- **Query:** Find the populations of London, Paris, Berlin and tell me which two are closest in size.
- **Shape:** planner
- **Final:** The populations of London, Paris, and Berlin are not provided in the input. Therefore, I cannot determine which two cities are closest in size.

### s8-d983be7d

- **Query:** Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory.
- **Shape:** planner
- **Final:** {"fields": {}, "rationale": "The input did not contain information about Claude Shannon's birth date, death date, or contributions to information theory."}

### s8-67888488

- **Query:** Find populations of London, Paris, and Berlin, then use Python to compute which two are closest in size.
- **Shape:** planner
- **Final:** (no final answer captured)

### s8-b2389077

- **Query:** Say hello.
- **Shape:** planner -> formatter(out)
- **Final:** Hello!

### s8-2d10cbcd

- **Query:** Say hello.
- **Shape:** planner
- **Final:** (no final answer captured)

---

## Skill usage across all sessions

| Skill | Sessions |
|-------|----------|
| planner | 49 |
| formatter | 47 |
| researcher | 22 |
| coder | 22 |
| sandbox_executor | 22 |
| critic | 15 |
| distiller | 13 |
| retriever | 6 |
| comparator | 5 |
| summariser | 2 |
