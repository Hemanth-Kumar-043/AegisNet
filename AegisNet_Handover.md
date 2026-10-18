# AegisNet Handover

Privacy-preserving cross-bank fraud detection for the IBM Z Datathon 2026 (Theme 2: AI Secured).
Status as of 18 Oct 2026 (updated after code review and the Alerts feature). Use together with `aegisnet.zip`.

## 1. What the project does

Three banks each hold transactions they may not share, and each mostly sees one kind of fraud. AegisNet builds one shared fraud model without moving any raw data.

1. **Local differential privacy.** Each bank clips its features to public bounds, scales them to [0,1], and adds Laplace noise (scale 1/ε) before training. ε is the privacy slider.
2. **Federated learning.** Each bank trains logistic regression locally. Federated averaging (FedAvg) merges the weights over several rounds.
3. **Secure aggregation.** Banks add pairwise random masks to their updates. The masks cancel in the sum, so the server gets the exact merged model but never a single bank's real update.
4. **Merge on LinuxONE.** The merge step is meant to run on the IBM LinuxONE VM (s390x).

Design change from the original submission: Random Forest has no averageable weights, so the model is now logistic regression. Random Forest can stay as a local baseline.

## 2. Measured results (synthetic data, ε=5, 10 rounds)

| Model | AUC |
|---|---|
| Bank A alone | 0.744 |
| Bank B alone | 0.803 |
| Bank C alone | 0.822 |
| Federated (all banks) | 0.833 |
| Pooled, no privacy (unsafe ceiling) | 0.856 |

Sweeping ε from 0.5 to no noise moves federated AUC from about 0.71 to 0.85. Masks cancel exactly (checked in `scripts/verify.py`).

## 3. Project layout

```
aegisnet/
  app.py                 router: page config, CSS, background, top navigation
  views/                 one file per page: home, federation, privacy, secure, data, linuxone
  static/                your IBM Z photos, cropped and tinted (served at /app/static, needs server.enableStaticServing)
  ui/                    theme.py, styles.py (CSS + animated background), components.py, icons.py (one SVG icon per page),
                         media.py (image banners, overview tiles, sidebar nav, how-to panels),
                         html_blocks.py (hero diagram + slider), shared.py (cached loaders, sidebar controls)
  core/                  data_gen.py, privacy.py, federated.py, secure_agg.py, platform_proof.py
  data/                  bank_a/b/c.csv, global_holdout_test.csv (synthetic)
  notebooks/             01_data_and_privacy, 02_federated_training, 03_secure_aggregation_and_linuxone_proof
  scripts/               verify.py, run_local.sh, setup_linuxone.sh, generate_dataset.py, build_notebooks.py
  Dockerfile, requirements.txt, README.md
```

## 4. Latest edit: the new UI

Requested: images, slideable content, fluid navigation between sections, and an animated background.

- **Multi-page navigation.** `app.py` uses `st.navigation(..., position="top")` with six pages: Overview, Federation, Privacy, Secure merge, Data, LinuxONE. This needs Streamlit 1.46 or newer.
- **Animated hero diagram** (`ui/html_blocks.py`, `hero_diagram`). Inline SVG: three bank boxes send packets along dashed lines into a pulsing LinuxONE shield. Packets change from amber (raw) to teal (masked) in transit.
- **Swipeable slider** (`slider`). Five slides: problem, noise, train locally, mask, merge. Arrows, dots, scroll and touch swiping.
- **Animated background** (`inject_background` in `ui/styles.py`). A drifting grid plus soft colored glows, pure CSS. It is disabled when the user prefers reduced motion.
- **Images** are inline SVG, so nothing external is needed. Hero and slider render in isolated iframes through `st.components.v1.html`, so their JS and animation do not depend on Streamlit's HTML sanitizer.
- **LinuxONE page** reads real facts from the machine (architecture, Secure Execution flag, CPU features) and says plainly when it is not running on s390x.
- No video file was added. The CSS background gives the same effect without a large asset. An optional MP4 slot can be added later.

**Not verified:** Streamlit was not installed in the sandbox where this was built, so the pages were compile-checked but never seen rendering. The backend and notebooks were executed and tested. Expect to fix visual issues on first run.

## 5. Run it locally (Mac, VS Code)

1. Unzip `aegisnet.zip`, delete any older `aegisnet` folder first.
2. VS Code: File > Open Folder > `aegisnet`, then Terminal > New Terminal.
3. Run `bash scripts/run_local.sh`. It creates `.venv`, installs requirements, prints the proof numbers, and starts the dashboard at `http://localhost:8501`.
4. If it prints nothing: the install is quiet and can take a minute or two. Otherwise run by hand:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python scripts/verify.py
   streamlit run app.py
   ```
5. If an old `.venv` exists, run `pip install -U streamlit` (the top menu needs 1.46+).

## 6. JupyterLab as the ML environment, LinuxONE VM as compute

Architecture: JupyterLab runs on the LinuxONE VM, so every notebook cell executes on s390x. The Mac is only a browser connected through an SSH tunnel.

**One-time setup on the VM**
```bash
scp -i <key.pem> ~/Downloads/aegisnet.zip <user>@<host>:~     # run on the Mac, not inside the VM
ssh -i <key.pem> -L 8888:localhost:8888 -L 8501:localhost:8501 <user>@<host>
unzip aegisnet.zip && cd aegisnet
tmux new -s lab
bash scripts/setup_linuxone.sh
```
The script installs build tools, creates `.venv`, installs requirements plus JupyterLab, registers the kernel `AegisNet (s390x)`, and starts JupyterLab on 127.0.0.1:8888. It uses `apt`; on RHEL or SLES install `python3-devel gcc gfortran openblas-devel` yourself and remove the `apt-get` line. Some packages compile on s390x, so the first install can take several minutes.

**Using it**
- Keep the SSH window with the `-L` flags open. Opening a second `ssh -L` just logs you into the VM again; the forwarding only works while that window stays open.
- On the Mac, open the `http://127.0.0.1:8888/lab?token=...` URL that Jupyter printed. Lost the token: `jupyter server list` on the VM.
- Run the notebooks in order and choose the kernel `AegisNet (s390x)`.
- Dashboard on the VM: `source .venv/bin/activate && streamlit run app.py --server.address 127.0.0.1 --server.port 8501`, then open `http://localhost:8501` on the Mac.

**Proof to capture for the submission** (notebook 03 and the LinuxONE page)
- `uname -m` prints `s390x`.
- `cat /sys/firmware/uv/prot_virt_guest` prints `1` only inside a Secure Execution guest. If it does not, do not claim Secure Execution. Say the aggregator runs on LinuxONE, or check whether the environment offers Secure Execution or Hyper Protect Virtual Servers.
- `lscpu` shows the machine generation. The Telum on-chip AI accelerator and quantum-safe crypto exist on z16-class machines (LinuxONE 4), not LinuxONE III. Verify the model before claiming either.
- Notebook 03 also benchmarks transaction scoring (latency and throughput). Save the executed notebook with outputs.

## 7. Problems already hit and their fixes

| Symptom | Cause and fix |
|---|---|
| `No such file` for `setup_linuxone.sh` | Wrong folder, or the zip was never uploaded. Run `pwd; ls`, `unzip aegisnet.zip`, `cd aegisnet`, then `bash scripts/setup_linuxone.sh`. |
| Zip not on the VM | `scp` must run from a Mac tab that is not inside the VM. |
| Tunnel logged into the VM and the link failed | Normal. Keep that window open and make sure JupyterLab is running. Check `ss -ltn | grep 8888`. |
| Port busy | Change the left number: `-L 8889:localhost:8888`. |
| `bash scripts/run_local.sh` shows nothing | Install is quiet; wait, or run the steps by hand (section 5). Check `pwd`, `python3 --version` (3.9+). |
| Venv not active, "No module named numpy" | Run `source .venv/bin/activate` and look for `(.venv)` in the prompt. |

## 8. Ideas to win the datathon

1. Run on real IBM Z and show `s390x` evidence from the executed notebook.
2. Real attestation: banks verify the aggregator before sending updates.
3. Membership-inference attack demo with and without differential privacy.
4. Add a real dataset (for example the Kaggle credit card fraud set) split across simulated banks.
5. Auditor page: privacy budget per round and an exportable compliance report (GDPR, PCI-DSS).
6. Malicious-bank test with robust aggregation (median or trimmed mean).
7. Scoring benchmark on LinuxONE versus an x86 VM; ONNX plus Telum acceleration only if the machine is z16-class.
8. Pitch order: each bank misses two of three fraud patterns alone, then the uplift, then the privacy proof, then the business case.

## 8b. Changes since the first handover

- **Alerts page** (`views/alerts.py`, `ui/alert_console.py`): scores international test transactions with the federated model, then an animated console (siren beacon, pulsing radar rings, dot-matrix world map, two hold-to-authorize keys, freeze, simulated police dispatch with a PII-free case file). Simulation only. `core/federated.py` now also returns `bias`.
- **Laundering page** (`views/laundering.py`, `ui/laundering_map.py`, `core/aml_cases.py`, `core/aml.py`): hop-by-hop animated route maps for Al Capone, BCCI, HSBC, Danske Bank Estonia, the Russian Laundromat and 1MDB (placement, layering, integration), a red-flag and prevention guide, and a rule-based scanner on a synthetic ledger (catches 8 of 8 planted schemes, 0 false positives). Case facts are simplified from public reports; routes are illustrative. The scanner does not use the federated model yet.
- **Motion polish** (`ui/styles.py`): nav links, buttons and tabs lift, enlarge and glow on hover; each page switch plays a veil fade and a rise-in. Disabled for reduced motion. The nav selectors (`stTopNavLink` etc.) are unverified against real Streamlit.
- **Review fixes:** dark theme in `.streamlit/config.toml`; hero SVG fixed height; header no longer forced `position:relative`; slider caption corrected; deprecated `use_container_width` removed (needs Streamlit 1.50+); no Secure Execution wording in hero, diagram or slides; privacy page states epsilon is per feature and labels are not noised; secure page states masks are simulated; `run_local.sh` no longer quiet; README and `.dockerignore` added; stray `{core,ui,scripts,data}` folder removed.
- **Image UI pass (18 Oct 2026):** your three IBM Z photos (z16 server, stage render, Z logo tile) are cropped and tinted navy in `static/` and used as page banners and overview tiles. Hover zooms the image slowly (banner) or lifts, glows and zooms (tile), like a console store page. `.streamlit/config.toml` now sets `enableStaticServing = true`; images load from `/app/static/...`, so keep that setting.
- **No emojis:** every page has its own line icon. Menu and tab icons use Streamlit's Material icons (`ui/icons.py`, `MATERIAL`); banners and tiles use custom inline SVGs (`icon()`).
- **Overview:** large image tiles for all seven other pages, each with an obvious "Open ..." button (`st.page_link`, keeps your sliders). The left sidebar also lists every page as a big link.
- **Instructions:** numbered "how to use" panels on Federation, Privacy, Alerts and Laundering; sidebar sliders have clearer labels and tooltips; the Alerts console shows a live 3-step guide (hold both keys, both say Authorized, press the red button).
- **Hover and buttons:** global buttons, page links, console keys, tabs, slider arrows and dots lift and glow on hover and shrink slightly when pressed.
- **Bug fixed:** the hold-to-authorize keys in the Alerts console cancelled themselves as soon as they were pressed (a child element of the key fired `pointerleave`). Now they fill and authorize. Tested in headless Chrome through the full block flow.
- **Not verified in real Streamlit (not installed in the sandbox):** the sidebar/page-link styling selectors (`stPageLink-NavLink`), the Material icon names, and the top-menu hover. If a tile's button looks unstyled or an icon is blank, tell me what you see.
- **Layout pass (18 Oct 2026, later):** the animated flow diagram now sits directly under the Overview banner, above the page tiles (Bank boxes widened so the text fits). A global `AEGISNET` title strip (`brand_title`) shows at the top of every page. A `ZeroDowntime` angular band (`zero_downtime`) sits between the KPI row and the slider on Overview. The top menu fades out when the page is scrolled past ~120px and the sidebar's page list slides in (`scroll_handoff` injects a small script into the parent page; the sidebar list lives in `st.container(key="aegisnav")`, needs Streamlit 1.39+). Unverified in real Streamlit: the top-menu element is found through `stTopNavLink`; if the top menu does not fade, that selector is the cause.
- **Sound + menu fix (18 Oct 2026, night):** the scroll hand-off now hides every top-menu link (it used to catch only the first). The Alerts console has a real siren (sawtooth wail, about 560-1240 Hz, level 0.28, stops on block, dismiss, tab change or after 14 s) that starts when a case above the threshold is open, and a rising four-note "verified" chime that plays when the simulated police acknowledgement arrives. Sound defaults to on with a toggle. Browsers may hold audio back until the first click; the console then shows a hint saying so. Tested in headless Chrome by counting audio nodes (siren starts and stops, chime plays); I could not listen to it, so check the volume on your machine.
- **Still unverified inside Streamlit:** the console and hero/slider HTML were rendered in headless Chrome, but the full multi-page app was not run in Streamlit. `pyarrow` may need compiling on s390x.

## 9. Open items

- Confirm the dashboard renders correctly (hero animation, slider, top menu, background) and fix any visual issues.
- Confirm which LinuxONE environment you have (Community Cloud, LinuxONE III or 4) and what it supports.
- Run notebook 03 on the VM and keep the output.
- Decide whether to add the attack demo, a real dataset, or the video background slot.
