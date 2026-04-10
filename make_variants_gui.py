#!/usr/bin/env python3

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
import subprocess
import shutil
import tempfile
import webbrowser
import xml.etree.ElementTree as ET
import numpy as np


# ============================================================
# リソースパス解決（開発時 / PyInstaller bundle 両対応）
# ============================================================

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


APP_ICON    = resource_path('SPERO_icon.ico')

# 設定ファイルは _internal（PyInstaller）またはスクリプトと同階層に保存
CONFIG_PATH = resource_path('bmd_variant_settings.json')

HOCOTATE_URL = 'https://github.com/Sadc2h4/Hocotate-Tool-Kit'

# Windows でコンソール非表示にするフラグ
CREATE_NO_WINDOW = 0x08000000


# ============================================================
# 設定ファイル
# ============================================================

def load_config():
    try:
        if os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_config(data):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ============================================================
# 多言語文字列定義
# ============================================================

STRINGS = {
    'ja': {
        # タブ
        'tab_main':               'メイン',
        'tab_scale_ranges':       'スケール範囲設定',
        # 言語バー
        'lang_label':             '言語:',
        # フォルダ枠
        'frm_folder':             'BMDフォルダ',
        'btn_browse':             '参照...',
        'dlg_browse':             'BMDファイルが入ったフォルダを選択',
        # ファイル一覧枠
        'frm_files':              '検出されたBMDファイル',
        'lbl_count':              '{n} 個のBMDファイルを検出',
        # 設定枠
        'frm_settings':           '設定',
        'lbl_variants':           'バリアント数:',
        'lbl_seed':               'シード値:',
        'chk_hide_cmd':           'CMDを非表示',
        'chk_select_one':         '出力結果を一つずつ選択',
        # スケール範囲枠
        'frm_scale_ranges':       'スケール範囲設定',
        'lbl_scale_min':          '最小',
        'lbl_scale_max':          '最大',
        'bone_head':              '頭',
        'bone_leaf':              '葉',
        'bone_body':              '体',
        'bone_leg':               '脚 (左右)',
        'bone_legcentre':         '脚中心',
        'bone_arm':               '腕 (左右)',
        'bone_eye':               '目',
        # 実行ボタン
        'btn_run':                '変換開始',
        # 進捗枠
        'frm_progress':           '進捗',
        'lbl_overall':            '全体:',
        'lbl_file':               'ファイル:',
        'status_idle':            '待機中',
        'status_running':         '変換中...',
        'status_done':            '完了',
        # ログ枠
        'frm_log':                'ログ',
        # 通常ダイアログ
        'err_no_folder':          'フォルダを選択してください。',
        'err_no_bmd':             'BMDファイルが見つかりません。',
        'dlg_done_title':         '完了',
        'dlg_done_msg':           '全ファイルの変換が完了しました。',
        'dlg_err_title':          'エラー',
        # Hocotate_Toolkit 未指定ダイアログ
        'hocotate_missing_title': 'Hocotate_Toolkit.exeが見つかりません',
        'hocotate_missing_msg': (
            'Hocotate_Toolkit.exeが見つかりません。\n\n'
            '下記GitHubからHocotate Toolkitをダウンロードし、\n'
            'ウィンドウ上部の「Hocotate_Toolkit.exe:」欄で\n'
            'Hocotate_Toolkit.exeのパスを指定してください。'
        ),
        'hocotate_missing_link':  'GitHubでHocotate Toolkitを入手する',
        # Hocotate パス指定バー
        'hocotate_path_label':    'Hocotate_Toolkit.exe:',
        'hocotate_path_browse':   '参照...',
        'hocotate_path_dlg':      'Hocotate_Toolkit.exeを選択',
        # ワーカーログ
        'w_sep':                  '=' * 52,
        'w_folder':               'フォルダ    : {v}',
        'w_count':                'BMDファイル : {v} 個',
        'w_params':               'バリアント数: {num}  シード: {seed}',
        'w_file':                 '\n[{idx}/{total}] {name}',
        'w_step1':                '  [1] BMD -> DAE 変換中...',
        'w_step1_ok':             '  DAE変換完了',
        'w_step1_err':            '  エラー: DAE変換失敗',
        'w_step2':                '  [2] DAE差分生成中 ({n}バリアント)...',
        'w_step2_ok':             '  DAE差分生成完了',
        'w_step3':                '  [3] BMD変換中...',
        'w_step3_ok':             '  完了: {ok}/{total} バリアント -> {path}',
        'w_step3_ok_select':      '  完了: 1/{total} バリアントを選択 -> {path}',
        'w_exception':            '  例外: {e}',
        'w_all_done':             '\n全ファイルの処理が完了しました。',
        'w_status':               '処理中 ({idx}/{total}): {name}',
    },
    'en': {
        # Tabs
        'tab_main':               'Main',
        'tab_scale_ranges':       'Scale Ranges',
        # Language bar
        'lang_label':             'Language:',
        # Folder frame
        'frm_folder':             'BMD Folder',
        'btn_browse':             'Browse...',
        'dlg_browse':             'Select a folder containing BMD files',
        # File list frame
        'frm_files':              'Detected BMD Files',
        'lbl_count':              '{n} BMD file(s) found',
        # Settings frame
        'frm_settings':           'Settings',
        'lbl_variants':           'Variants:',
        'lbl_seed':               'Seed:',
        'chk_hide_cmd':           'Hide CMD window',
        'chk_select_one':         'Select one output per type',
        # Scale ranges frame
        'frm_scale_ranges':       'Scale Ranges',
        'lbl_scale_min':          'Min',
        'lbl_scale_max':          'Max',
        'bone_head':              'Head',
        'bone_leaf':              'Leaf',
        'bone_body':              'Body',
        'bone_leg':               'Legs (L+R)',
        'bone_legcentre':         'Leg Centre',
        'bone_arm':               'Arms (L+R)',
        'bone_eye':               'Eye',
        # Run button
        'btn_run':                'Start Conversion',
        # Progress frame
        'frm_progress':           'Progress',
        'lbl_overall':            'Overall:',
        'lbl_file':               'File:',
        'status_idle':            'Idle',
        'status_running':         'Converting...',
        'status_done':            'Done',
        # Log frame
        'frm_log':                'Log',
        # Normal dialogs
        'err_no_folder':          'Please select a folder.',
        'err_no_bmd':             'No BMD files found.',
        'dlg_done_title':         'Done',
        'dlg_done_msg':           'All files converted successfully.',
        'dlg_err_title':          'Error',
        # Hocotate_Toolkit missing dialog
        'hocotate_missing_title': 'Hocotate_Toolkit.exe Not Found',
        'hocotate_missing_msg': (
            'Hocotate_Toolkit.exe could not be found.\n\n'
            'Download Hocotate Toolkit from GitHub and specify\n'
            'the path to Hocotate_Toolkit.exe using the\n'
            '"Hocotate_Toolkit.exe:" field at the top of the window.'
        ),
        'hocotate_missing_link':  'Get Hocotate Toolkit on GitHub',
        # Hocotate path bar
        'hocotate_path_label':    'Hocotate_Toolkit.exe:',
        'hocotate_path_browse':   'Browse...',
        'hocotate_path_dlg':      'Select Hocotate_Toolkit.exe',
        # Worker log
        'w_sep':                  '=' * 52,
        'w_folder':               'Folder    : {v}',
        'w_count':                'BMD files : {v}',
        'w_params':               'Variants  : {num}  Seed: {seed}',
        'w_file':                 '\n[{idx}/{total}] {name}',
        'w_step1':                '  [1] BMD -> DAE ...',
        'w_step1_ok':             '  DAE conversion complete',
        'w_step1_err':            '  Error: DAE conversion failed',
        'w_step2':                '  [2] Generating DAE variants ({n})...',
        'w_step2_ok':             '  DAE variants generated',
        'w_step3':                '  [3] Converting to BMD...',
        'w_step3_ok':             '  Done: {ok}/{total} variants -> {path}',
        'w_step3_ok_select':      '  Done: 1/{total} variant selected -> {path}',
        'w_exception':            '  Exception: {e}',
        'w_all_done':             '\nAll files converted.',
        'w_status':               'Processing ({idx}/{total}): {name}',
    },
}

LANG_DISPLAY      = ['日本語', 'English']
LANG_CODE         = {'日本語': 'ja', 'English': 'en'}
LANG_DISPLAY_CODE = {'ja': '日本語', 'en': 'English'}


# ============================================================
# 変換ロジック
# ============================================================

BONE_GROUPS = {
    'head':      ['headjnt'],
    'leaf':      ['happajnt1', 'happajnt2', 'happajnt3'],
    'body':      ['sebonjnt'],
    'leg':       ['llegjnt', 'rlegjnt'],
    'legcentre': ['legcentre'],
    'arm':       ['lhandjnt', 'rhandjnt'],
    # 'eye' は bone ではなくメッシュで処理するため BONE_GROUPS に含めない
}

BONE_GROUP_ORDER = [
    'head', 'leaf', 'body',
    'leg', 'legcentre',
    'arm', 'eye',
]

DEFAULT_SCALE_RANGES = {
    'head':      (0.75, 1.40),
    'leaf':      (0.60, 1.60),
    'body':      (0.80, 1.25),
    'leg':       (0.70, 1.40),
    'legcentre': (0.85, 1.15),
    'arm':       (0.70, 1.40),
    'eye':       (0.80, 1.30),
}


def _ns_tag(ns, name):
    return f'{{{ns}}}{name}' if ns else name

def _get_namespace(root):
    t = root.tag
    return t[1:t.index('}')] if t.startswith('{') else ''

def _parse_floats(text):
    return [float(x) for x in text.split()]

def _get_bone_assignments(skin_elem, ns):
    name_arr = skin_elem.find(f'.//{_ns_tag(ns, "Name_array")}')
    if name_arr is None or not name_arr.text:
        return []
    joint_names = name_arr.text.split()
    vw = skin_elem.find(f'.//{_ns_tag(ns, "vertex_weights")}')
    if vw is None:
        return []
    vc_elem = vw.find(_ns_tag(ns, 'vcount'))
    v_elem  = vw.find(_ns_tag(ns, 'v'))
    if vc_elem is None or v_elem is None:
        return []
    vcount = [int(x) for x in vc_elem.text.split()]
    v      = [int(x) for x in v_elem.text.split()]
    result, offset = [], 0
    for count in vcount:
        if count == 0:
            result.append(None)
        else:
            result.append(joint_names[v[offset]])
            offset += count * 2
    return result

def generate_scales(rng, scale_ranges):
    return {g: rng.uniform(lo, hi) for g, (lo, hi) in scale_ranges.items()}

def apply_scales_to_dae(input_path, output_path, scales):
    ET.register_namespace('', 'http://www.collada.org/2005/11/COLLADASchema')
    tree = ET.parse(input_path)
    root = tree.getroot()
    ns   = _get_namespace(root)

    geom_to_skin = {}
    lib_ctrl = root.find(f'.//{_ns_tag(ns, "library_controllers")}')
    if lib_ctrl is not None:
        for ctrl in lib_ctrl.findall(_ns_tag(ns, 'controller')):
            skin = ctrl.find(_ns_tag(ns, 'skin'))
            if skin is not None:
                src_id = skin.attrib.get('source', '').lstrip('#')
                geom_to_skin[src_id] = skin

    lib_geom = root.find(f'.//{_ns_tag(ns, "library_geometries")}')
    if lib_geom is None:
        tree.write(output_path, xml_declaration=True, encoding='unicode')
        return

    head_bones = set(BONE_GROUPS.get('head', []))

    # ---- Pass 1: 頭のセントロイドを取得（目の位置補正に使用） ----
    head_centroid = None
    for geom in lib_geom.findall(_ns_tag(ns, 'geometry')):
        skin = geom_to_skin.get(geom.attrib.get('id', ''))
        if skin is None:
            continue
        bone_asgn = _get_bone_assignments(skin, ns)
        bone_set  = {b for b in bone_asgn if b is not None}
        if len(bone_set) <= 1:
            continue  # 複数ボーンのメッシュ（ボディ）のみ対象
        mesh_elem = geom.find(_ns_tag(ns, 'mesh'))
        if mesh_elem is None:
            continue
        for src in mesh_elem.findall(_ns_tag(ns, 'source')):
            if 'positions' not in src.attrib.get('id', ''):
                continue
            fa = src.find(_ns_tag(ns, 'float_array'))
            if fa is None or not fa.text:
                continue
            positions = np.array(_parse_floats(fa.text), dtype=np.float64).reshape(-1, 3)
            head_idxs = [vi for vi, b in enumerate(bone_asgn)
                         if vi < len(positions) and b in head_bones]
            if head_idxs:
                head_centroid = positions[np.array(head_idxs)].mean(axis=0)
            break
        if head_centroid is not None:
            break

    # ---- Pass 2: スケール適用 ----
    for geom in lib_geom.findall(_ns_tag(ns, 'geometry')):
        skin = geom_to_skin.get(geom.attrib.get('id', ''))
        if skin is None:
            continue
        bone_asgn = _get_bone_assignments(skin, ns)
        if not bone_asgn:
            continue
        mesh_elem = geom.find(_ns_tag(ns, 'mesh'))
        if mesh_elem is None:
            continue

        bone_set    = {b for b in bone_asgn if b is not None}
        # 目メッシュ判定: 全頂点が head ボーンのみにスキニングされているメッシュ
        # (head_centroid が取得できた = ボディメッシュが存在する場合のみ有効)
        is_eye_mesh = (bool(bone_set) and bone_set.issubset(head_bones)
                       and head_centroid is not None)

        for src in mesh_elem.findall(_ns_tag(ns, 'source')):
            if 'positions' not in src.attrib.get('id', ''):
                continue
            fa = src.find(_ns_tag(ns, 'float_array'))
            if fa is None or not fa.text:
                continue
            positions = np.array(_parse_floats(fa.text), dtype=np.float64).reshape(-1, 3)
            n = positions.shape[0]

            if is_eye_mesh:
                # 目の中心を頭のスケールに追従させ、目自体のサイズをスケール
                head_scale = scales.get('head', 1.0)
                eye_scale  = scales.get('eye',  1.0)
                eye_center = positions.mean(axis=0)
                new_eye_center = head_centroid + (eye_center - head_centroid) * head_scale
                positions = new_eye_center + (positions - eye_center) * eye_scale
            else:
                grp_idx = {g: [] for g in BONE_GROUPS}
                for vi in range(min(n, len(bone_asgn))):
                    bone = bone_asgn[vi]
                    if bone is None:
                        continue
                    for grp, blist in BONE_GROUPS.items():
                        if bone in blist:
                            grp_idx[grp].append(vi)
                            break
                for grp, idxs in grp_idx.items():
                    if not idxs:
                        continue
                    s = scales.get(grp, 1.0)
                    if abs(s - 1.0) < 1e-9:
                        continue
                    arr = np.array(idxs)
                    pts = positions[arr]
                    centroid = pts.mean(axis=0)
                    positions[arr] = centroid + (pts - centroid) * s

            fa.text = ' '.join(f'{v:.7g}' for v in positions.flatten())

        for src in mesh_elem.findall(_ns_tag(ns, 'source')):
            if 'normals' not in src.attrib.get('id', ''):
                continue
            fa = src.find(_ns_tag(ns, 'float_array'))
            if fa is None or not fa.text:
                continue
            normals = np.array(_parse_floats(fa.text), dtype=np.float64).reshape(-1, 3)
            norms   = np.linalg.norm(normals, axis=1, keepdims=True)
            normals /= np.where(norms < 1e-8, 1.0, norms)
            fa.text = ' '.join(f'{v:.7g}' for v in normals.flatten())

    tree.write(output_path, xml_declaration=True, encoding='unicode')


# ============================================================
# 変換ワーカー（バックグラウンドスレッド）
# ============================================================

MSG_LOG     = 'log'
MSG_OVERALL = 'progress_overall'
MSG_FILE    = 'progress_file'
MSG_STATUS  = 'status'
MSG_DONE    = 'done'
MSG_ERROR   = 'error'


def conversion_worker(bmd_files, input_dir, num_variants, seed, hide_cmd, scale_ranges,
                      select_one, S, q, hocotate_exe):
    sub_kwargs = dict(capture_output=True, text=True)
    if hide_cmd and sys.platform == 'win32':
        sub_kwargs['creationflags'] = CREATE_NO_WINDOW

    total         = len(bmd_files)
    rng           = np.random.default_rng(seed)
    variants_root = os.path.join(input_dir, 'variants')
    selected_root = os.path.join(input_dir, 'selected')

    if select_one:
        os.makedirs(selected_root, exist_ok=True)

    for idx, bmd_name in enumerate(bmd_files):
        base     = os.path.splitext(bmd_name)[0]
        bmd_path = os.path.join(input_dir, bmd_name)
        out_dir  = os.path.join(variants_root, base)

        q.put((MSG_LOG,    S['w_file'].format(idx=idx+1, total=total, name=bmd_name)))
        q.put((MSG_STATUS, S['w_status'].format(idx=idx+1, total=total, name=bmd_name)))
        q.put((MSG_FILE,   0))

        workdir = tempfile.mkdtemp(prefix=f'bmdvar_{base}_')

        try:
            if not select_one:
                os.makedirs(out_dir, exist_ok=True)
            shutil.copy2(bmd_path, workdir)

            # ---- Step 1: BMD → DAE (0-20%) ----
            q.put((MSG_LOG,  S['w_step1']))
            q.put((MSG_FILE, 5))

            dae_path = os.path.join(workdir, f'{base}.dae')
            proc     = subprocess.run(
                [hocotate_exe, '--bmd2dae',
                 os.path.join(workdir, bmd_name), dae_path],
                **sub_kwargs)

            if not os.path.isfile(dae_path):
                q.put((MSG_LOG, S['w_step1_err']))
                q.put((MSG_LOG, proc.stdout[-400:] if proc.stdout else ''))
                continue

            mat_json = os.path.join(workdir, f'{base}_materials.json')
            tex_json = os.path.join(workdir, f'{base}_tex_headers.json')
            q.put((MSG_LOG,  S['w_step1_ok']))
            q.put((MSG_FILE, 20))

            # ---- Step 2: DAE差分生成 (20-50%) ----
            q.put((MSG_LOG,  S['w_step2'].format(n=num_variants)))
            var_work = os.path.join(workdir, 'variants')
            os.makedirs(var_work, exist_ok=True)

            for f in os.listdir(workdir):
                if f.lower().endswith('.png'):
                    shutil.copy2(os.path.join(workdir, f), var_work)

            for i in range(1, num_variants + 1):
                vnum    = f'{i:02d}'
                scales  = generate_scales(rng, scale_ranges)
                out_dae = os.path.join(var_work, f'{base}_var{vnum}.dae')
                apply_scales_to_dae(dae_path, out_dae, scales)
                q.put((MSG_FILE, 20 + int(i / num_variants * 30)))

            q.put((MSG_LOG, S['w_step2_ok']))

            # ---- Step 3: 差分DAE → BMD (50-100%) ----
            q.put((MSG_LOG, S['w_step3']))
            ok = 0

            if select_one:
                # 生成したDAEの中からランダムに1つ選んでBMD変換し selected/ へ出力
                available = [
                    os.path.join(var_work, f'{base}_var{i:02d}.dae')
                    for i in range(1, num_variants + 1)
                    if os.path.isfile(os.path.join(var_work, f'{base}_var{i:02d}.dae'))
                ]
                if available:
                    chosen_dae = available[int(rng.integers(0, len(available)))]
                    dest_bmd   = os.path.join(selected_root, f'{base}.bmd')

                    cmd = [hocotate_exe, '--dae2bmd', chosen_dae, dest_bmd]
                    if os.path.isfile(mat_json):
                        cmd += ['--mat',       mat_json]
                    if os.path.isfile(tex_json):
                        cmd += ['--texheader', tex_json]

                    subprocess.run(cmd, **sub_kwargs)
                    if os.path.isfile(dest_bmd):
                        ok = 1

                q.put((MSG_FILE, 100))
                q.put((MSG_LOG, S['w_step3_ok_select'].format(
                    total=num_variants, path=os.path.join(selected_root, f'{base}.bmd'))))

            else:
                # 通常モード: 全バリアントを variants/{base}/ へ出力
                for i in range(1, num_variants + 1):
                    vnum    = f'{i:02d}'
                    var_dae = os.path.join(var_work, f'{base}_var{vnum}.dae')
                    var_bmd = os.path.join(out_dir,  f'{base}_var{vnum}.bmd')

                    if not os.path.isfile(var_dae):
                        continue

                    cmd = [hocotate_exe, '--dae2bmd', var_dae, var_bmd]
                    if os.path.isfile(mat_json):
                        cmd += ['--mat',       mat_json]
                    if os.path.isfile(tex_json):
                        cmd += ['--texheader', tex_json]

                    subprocess.run(cmd, **sub_kwargs)
                    if os.path.isfile(var_bmd):
                        ok += 1

                    q.put((MSG_FILE, 50 + int(i / num_variants * 50)))

                q.put((MSG_LOG, S['w_step3_ok'].format(ok=ok, total=num_variants, path=out_dir)))

        except Exception as e:
            q.put((MSG_LOG, S['w_exception'].format(e=e)))

        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        q.put((MSG_OVERALL, int((idx + 1) / total * 100)))

    q.put((MSG_FILE,   100))
    q.put((MSG_STATUS, S['status_done']))
    q.put((MSG_LOG,    S['w_all_done']))
    q.put((MSG_DONE,   None))


# ============================================================
# GUI
# ============================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PikiModel_Randomizer')
        self.resizable(False, False)

        if os.path.isfile(APP_ICON):
            try:
                self.iconbitmap(APP_ICON)
            except Exception:
                pass

        self._current_lang  = 'ja'
        self._current_count = 0
        self._running       = False
        self._q             = queue.Queue()

        # 設定ファイルを先に読み込んで言語を確定する
        # （Hocotate 未検出ダイアログより前に言語を反映させるため）
        cfg = load_config()
        if cfg.get('language') in STRINGS:
            self._current_lang = cfg['language']

        self._build_ui()
        self._restore_from_config(cfg)
        self._apply_lang()

        self.protocol('WM_DELETE_WINDOW', self._on_closing)

        # ウィンドウ描画後に Hocotate_Toolkit の存在をチェック
        self.after(150, self._check_hocotate)

    # ----------------------------------------------------------
    # 設定の保存 / 復元
    # ----------------------------------------------------------
    def _save_settings(self):
        scale_ranges = {}
        for grp in BONE_GROUP_ORDER:
            lo = self._scale_min_vars[grp].get()
            hi = self._scale_max_vars[grp].get()
            scale_ranges[grp] = [round(lo, 3), round(hi, 3)]
        save_config({
            'language':      self._current_lang,
            'hocotate_path': self._var_hocotate_path.get(),
            'variants':      self._var_num.get(),
            'seed':          self._var_seed.get(),
            'hide_cmd':      self._var_hide_cmd.get(),
            'select_one':    self._var_select_one.get(),
            'scale_ranges':  scale_ranges,
        })

    def _restore_from_config(self, cfg):
        if cfg.get('language') in STRINGS:
            self._cmb_lang.set(LANG_DISPLAY_CODE[cfg['language']])
        if 'hocotate_path' in cfg:
            self._var_hocotate_path.set(cfg['hocotate_path'])
        if 'variants' in cfg:
            self._var_num.set(int(cfg['variants']))
        if 'seed' in cfg:
            self._var_seed.set(int(cfg['seed']))
        if 'hide_cmd' in cfg:
            self._var_hide_cmd.set(bool(cfg['hide_cmd']))
        if 'select_one' in cfg:
            self._var_select_one.set(bool(cfg['select_one']))
        if 'scale_ranges' in cfg:
            sr = cfg['scale_ranges']
            # 旧バージョンの left_leg/right_leg/left_arm/right_arm キーを移行
            for old_l, old_r, new_key in [
                ('left_leg', 'right_leg', 'leg'),
                ('left_arm', 'right_arm', 'arm'),
            ]:
                if new_key not in sr:
                    if old_l in sr:
                        sr[new_key] = sr[old_l]
                    elif old_r in sr:
                        sr[new_key] = sr[old_r]
            for grp in BONE_GROUP_ORDER:
                if grp in sr:
                    val = sr[grp]
                    if isinstance(val, (list, tuple)) and len(val) == 2:
                        self._scale_min_vars[grp].set(round(float(val[0]), 3))
                        self._scale_max_vars[grp].set(round(float(val[1]), 3))

    def _on_closing(self):
        self._save_settings()
        self.destroy()

    # ----------------------------------------------------------
    # 翻訳ヘルパー
    # ----------------------------------------------------------
    def _t(self, key, **kwargs):
        s = STRINGS[self._current_lang].get(key, key)
        return s.format(**kwargs) if kwargs else s

    # ----------------------------------------------------------
    # Hocotate_Toolkit 存在確認
    # ----------------------------------------------------------
    def _check_hocotate(self):
        path = self._var_hocotate_path.get().strip()
        if not path or not os.path.isfile(path):
            self._show_hocotate_missing_dialog()
            return False
        return True

    def _show_hocotate_missing_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title(self._t('hocotate_missing_title'))
        dlg.resizable(False, False)
        dlg.grab_set()

        if os.path.isfile(APP_ICON):
            try:
                dlg.iconbitmap(APP_ICON)
            except Exception:
                pass

        ttk.Label(
            dlg,
            text=self._t('hocotate_missing_title'),
            font=('', 10, 'bold'),
            foreground='#cc3300',
        ).pack(padx=20, pady=(16, 4))

        ttk.Separator(dlg, orient='horizontal').pack(fill='x', padx=12, pady=4)

        ttk.Label(
            dlg,
            text=self._t('hocotate_missing_msg'),
            justify='left',
        ).pack(padx=20, pady=(4, 10))

        lbl_link = tk.Label(
            dlg,
            text=self._t('hocotate_missing_link'),
            fg='#0055cc',
            cursor='hand2',
            font=('', 9, 'underline'),
        )
        lbl_link.pack(pady=(0, 12))
        lbl_link.bind('<Button-1>', lambda _e: webbrowser.open(HOCOTATE_URL))

        ttk.Separator(dlg, orient='horizontal').pack(fill='x', padx=12, pady=(0, 4))

        ttk.Button(dlg, text='OK', width=10,
                   command=dlg.destroy).pack(pady=(4, 14))

        dlg.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - dlg.winfo_width())  // 2
        y = self.winfo_y() + (self.winfo_height() - dlg.winfo_height()) // 2
        dlg.geometry(f'+{x}+{y}')

    # ----------------------------------------------------------
    # UI 構築
    # ----------------------------------------------------------
    def _build_ui(self):
        P = dict(padx=8, pady=4)

        # ---- 言語バー + Hocotate パス指定（タブ外・常時表示） ----
        frm_lang = ttk.Frame(self)
        frm_lang.pack(fill='x', padx=8, pady=(8, 2))

        self._lbl_lang = ttk.Label(frm_lang, text='')
        self._lbl_lang.pack(side='left')

        self._cmb_lang = ttk.Combobox(
            frm_lang, values=LANG_DISPLAY, state='readonly', width=10)
        self._cmb_lang.set('日本語')
        self._cmb_lang.pack(side='left', padx=(4, 0))
        self._cmb_lang.bind('<<ComboboxSelected>>', self._on_lang_change)

        ttk.Separator(frm_lang, orient='vertical').pack(
            side='left', fill='y', padx=(12, 8), pady=2)

        self._lbl_hocotate = ttk.Label(frm_lang, text='')
        self._lbl_hocotate.pack(side='left')

        self._var_hocotate_path = tk.StringVar()
        self._ent_hocotate = ttk.Entry(
            frm_lang, textvariable=self._var_hocotate_path,
            width=36, state='readonly')
        self._ent_hocotate.pack(side='left', padx=(4, 4))

        self._btn_hocotate_browse = ttk.Button(
            frm_lang, text='', width=8, command=self._browse_hocotate)
        self._btn_hocotate_browse.pack(side='left')

        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=8, pady=(4, 0))

        # ---- タブコンテナ ----
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill='both', expand=True, padx=8, pady=4)

        # Tab 0: メイン
        self._tab_main = ttk.Frame(self._notebook, padding=4)
        self._notebook.add(self._tab_main, text='')

        # Tab 1: スケール範囲設定
        self._tab_scale = ttk.Frame(self._notebook, padding=4)
        self._notebook.add(self._tab_scale, text='')

        self._build_main_tab(P)
        self._build_scale_tab(P)

    def _build_main_tab(self, P):
        tab = self._tab_main

        # ---- フォルダ選択 ----
        self._frm_folder = ttk.LabelFrame(tab, text='', padding=6)
        self._frm_folder.pack(fill='x', padx=4, pady=4)

        self._var_folder = tk.StringVar()
        ttk.Entry(self._frm_folder, textvariable=self._var_folder,
                  width=52, state='readonly').pack(side='left', fill='x', expand=True)
        self._btn_browse = ttk.Button(
            self._frm_folder, text='', width=8, command=self._browse)
        self._btn_browse.pack(side='left', padx=(6, 0))

        # ---- ファイルリスト ----
        self._frm_files = ttk.LabelFrame(tab, text='', padding=6)
        self._frm_files.pack(fill='both', expand=True, padx=4, pady=4)

        sb = ttk.Scrollbar(self._frm_files, orient='vertical')
        self._listbox = tk.Listbox(
            self._frm_files, height=6, yscrollcommand=sb.set,
            activestyle='none', selectbackground='#cde8ff')
        sb.config(command=self._listbox.yview)
        self._listbox.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        self._lbl_count = ttk.Label(self._frm_files, text='')
        self._lbl_count.pack(anchor='w', pady=(4, 0))

        # ---- 基本設定 ----
        self._frm_cfg = ttk.LabelFrame(tab, text='', padding=6)
        self._frm_cfg.pack(fill='x', padx=4, pady=4)

        self._lbl_variants = ttk.Label(self._frm_cfg, text='')
        self._lbl_variants.grid(row=0, column=0, sticky='w')
        self._var_num = tk.IntVar(value=10)
        ttk.Spinbox(self._frm_cfg, from_=1, to=50,
                    textvariable=self._var_num, width=5).grid(
            row=0, column=1, sticky='w', padx=(4, 20))

        self._lbl_seed = ttk.Label(self._frm_cfg, text='')
        self._lbl_seed.grid(row=0, column=2, sticky='w')
        self._var_seed = tk.IntVar(value=42)
        ttk.Spinbox(self._frm_cfg, from_=0, to=99999,
                    textvariable=self._var_seed, width=7).grid(
            row=0, column=3, sticky='w', padx=4)

        self._var_hide_cmd = tk.BooleanVar(value=True)
        self._chk_hide_cmd = ttk.Checkbutton(
            self._frm_cfg, text='', variable=self._var_hide_cmd)
        self._chk_hide_cmd.grid(row=1, column=0, columnspan=4,
                                sticky='w', pady=(6, 0))

        self._var_select_one = tk.BooleanVar(value=False)
        self._chk_select_one = ttk.Checkbutton(
            self._frm_cfg, text='', variable=self._var_select_one)
        self._chk_select_one.grid(row=2, column=0, columnspan=4,
                                  sticky='w', pady=(2, 0))

        # ---- 実行ボタン ----
        self._btn_run = ttk.Button(tab, text='', width=16, command=self._start)
        self._btn_run.pack(pady=(6, 2))

        # ---- 進捗 ----
        self._frm_prog = ttk.LabelFrame(tab, text='', padding=6)
        self._frm_prog.pack(fill='x', padx=4, pady=4)

        self._lbl_overall_hdr = ttk.Label(self._frm_prog, text='', width=9, anchor='w')
        self._lbl_overall_hdr.grid(row=0, column=0, sticky='w')
        self._pb_overall = ttk.Progressbar(
            self._frm_prog, length=320, maximum=100, mode='determinate')
        self._pb_overall.grid(row=0, column=1, sticky='ew', padx=4, pady=2)
        self._lbl_pct_overall = ttk.Label(
            self._frm_prog, text='  0%', width=5, anchor='e')
        self._lbl_pct_overall.grid(row=0, column=2)

        self._lbl_file_hdr = ttk.Label(self._frm_prog, text='', width=9, anchor='w')
        self._lbl_file_hdr.grid(row=1, column=0, sticky='w')
        self._pb_file = ttk.Progressbar(
            self._frm_prog, length=320, maximum=100, mode='determinate')
        self._pb_file.grid(row=1, column=1, sticky='ew', padx=4, pady=2)
        self._lbl_pct_file = ttk.Label(
            self._frm_prog, text='  0%', width=5, anchor='e')
        self._lbl_pct_file.grid(row=1, column=2)

        self._lbl_status = ttk.Label(self._frm_prog, text='', foreground='#555')
        self._lbl_status.grid(row=2, column=0, columnspan=3,
                              sticky='w', pady=(4, 0))
        self._frm_prog.columnconfigure(1, weight=1)

        # ---- ログ ----
        self._frm_log = ttk.LabelFrame(tab, text='', padding=6)
        self._frm_log.pack(fill='both', expand=True, padx=4, pady=4)

        self._log = scrolledtext.ScrolledText(
            self._frm_log, height=8, state='disabled',
            wrap='word', font=('Consolas', 9))
        self._log.pack(fill='both', expand=True)

    def _build_scale_tab(self, P):
        tab = self._tab_scale

        self._frm_scale = ttk.LabelFrame(tab, text='', padding=10)
        self._frm_scale.pack(fill='both', expand=True, padx=4, pady=4)

        # ヘッダー行
        # col 0: ボーン名, col 1: min spinbox, col 2: "~", col 3: max spinbox, col 4: 対称注記
        self._lbl_scale_header_min = ttk.Label(
            self._frm_scale, text='', foreground='#555')
        self._lbl_scale_header_min.grid(row=0, column=1, sticky='w', padx=(4, 2), pady=(0, 4))
        self._lbl_scale_header_max = ttk.Label(
            self._frm_scale, text='', foreground='#555')
        self._lbl_scale_header_max.grid(row=0, column=3, sticky='w', padx=(2, 4), pady=(0, 4))

        self._scale_min_vars    = {}
        self._scale_max_vars    = {}
        self._scale_lbl_widgets = {}

        for row_i, grp in enumerate(BONE_GROUP_ORDER, start=1):
            lo_def, hi_def = DEFAULT_SCALE_RANGES[grp]
            min_var = tk.DoubleVar(value=lo_def)
            max_var = tk.DoubleVar(value=hi_def)
            self._scale_min_vars[grp] = min_var
            self._scale_max_vars[grp] = max_var

            lbl = ttk.Label(self._frm_scale, text='', width=11, anchor='w')
            lbl.grid(row=row_i, column=0, sticky='w', padx=(0, 4), pady=3)
            self._scale_lbl_widgets[grp] = lbl

            ttk.Spinbox(
                self._frm_scale,
                from_=0.01, to=5.0, increment=0.05,
                textvariable=min_var, width=6, format='%.2f',
            ).grid(row=row_i, column=1, sticky='w', padx=(4, 2), pady=3)

            ttk.Label(self._frm_scale, text='~').grid(
                row=row_i, column=2, padx=2)

            ttk.Spinbox(
                self._frm_scale,
                from_=0.01, to=5.0, increment=0.05,
                textvariable=max_var, width=6, format='%.2f',
            ).grid(row=row_i, column=3, sticky='w', padx=(2, 4), pady=3)

    # ----------------------------------------------------------
    # 言語適用
    # ----------------------------------------------------------
    def _apply_lang(self):
        t = self._t
        # タブラベル
        self._notebook.tab(0, text=t('tab_main'))
        self._notebook.tab(1, text=t('tab_scale_ranges'))
        # 言語バー / Hocotate パス欄
        self._lbl_lang.config(text=t('lang_label'))
        self._lbl_hocotate.config(text=t('hocotate_path_label'))
        self._btn_hocotate_browse.config(text=t('hocotate_path_browse'))
        # メインタブ
        self._frm_folder.config(text=t('frm_folder'))
        self._btn_browse.config(text=t('btn_browse'))
        self._frm_files.config(text=t('frm_files'))
        self._lbl_count.config(text=t('lbl_count', n=self._current_count))
        self._frm_cfg.config(text=t('frm_settings'))
        self._lbl_variants.config(text=t('lbl_variants'))
        self._lbl_seed.config(text=t('lbl_seed'))
        self._chk_hide_cmd.config(text=t('chk_hide_cmd'))
        self._chk_select_one.config(text=t('chk_select_one'))
        self._btn_run.config(text=t('btn_run'))
        self._frm_prog.config(text=t('frm_progress'))
        self._lbl_overall_hdr.config(text=t('lbl_overall'))
        self._lbl_file_hdr.config(text=t('lbl_file'))
        self._frm_log.config(text=t('frm_log'))
        if not self._running:
            self._lbl_status.config(text=t('status_idle'))
        # スケール範囲タブ
        self._frm_scale.config(text=t('frm_scale_ranges'))
        self._lbl_scale_header_min.config(text=t('lbl_scale_min'))
        self._lbl_scale_header_max.config(text=t('lbl_scale_max'))
        for grp in BONE_GROUP_ORDER:
            self._scale_lbl_widgets[grp].config(text=t(f'bone_{grp}'))

    # ----------------------------------------------------------
    # 言語変更
    # ----------------------------------------------------------
    def _on_lang_change(self, _event=None):
        self._current_lang = LANG_CODE.get(self._cmb_lang.get(), 'ja')
        self._apply_lang()
        self._save_settings()

    # ----------------------------------------------------------
    # Hocotate_Toolkit.exe パス指定
    # ----------------------------------------------------------
    def _browse_hocotate(self):
        path = filedialog.askopenfilename(
            title=self._t('hocotate_path_dlg'),
            filetypes=[('Executable', 'Hocotate_Toolkit.exe'), ('All files', '*.*')],
        )
        if not path:
            return
        self._var_hocotate_path.set(path)
        self._save_settings()

    # ----------------------------------------------------------
    # フォルダ選択
    # ----------------------------------------------------------
    def _browse(self):
        folder = filedialog.askdirectory(title=self._t('dlg_browse'))
        if not folder:
            return
        self._var_folder.set(folder)
        files = sorted(f for f in os.listdir(folder) if f.lower().endswith('.bmd'))
        self._listbox.delete(0, 'end')
        for f in files:
            self._listbox.insert('end', f)
        self._current_count = len(files)
        self._lbl_count.config(text=self._t('lbl_count', n=self._current_count))

    # ----------------------------------------------------------
    # スケール範囲を取得（min > max の場合は自動入れ替え）
    # ----------------------------------------------------------
    def _get_scale_ranges(self):
        ranges = {}
        for grp in BONE_GROUP_ORDER:
            lo = self._scale_min_vars[grp].get()
            hi = self._scale_max_vars[grp].get()
            if lo > hi:
                lo, hi = hi, lo
            ranges[grp] = (lo, hi)
        return ranges

    # ----------------------------------------------------------
    # 変換開始
    # ----------------------------------------------------------
    def _start(self):
        if self._running:
            return

        if not self._check_hocotate():
            return

        folder = self._var_folder.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror(self._t('dlg_err_title'), self._t('err_no_folder'))
            return

        bmd_files = sorted(f for f in os.listdir(folder) if f.lower().endswith('.bmd'))
        if not bmd_files:
            messagebox.showwarning(self._t('dlg_err_title'), self._t('err_no_bmd'))
            return

        S = STRINGS[self._current_lang]
        scale_ranges = self._get_scale_ranges()

        self._running = True
        self._btn_run.config(state='disabled')
        self._pb_overall['value'] = 0
        self._pb_file['value']    = 0
        self._lbl_pct_overall.config(text='  0%')
        self._lbl_pct_file.config(text='  0%')
        self._lbl_status.config(text=self._t('status_running'))

        self._log_append('\n' + S['w_sep'])
        self._log_append(S['w_folder'].format(v=folder))
        self._log_append(S['w_count'].format(v=len(bmd_files)))
        self._log_append(S['w_params'].format(
            num=self._var_num.get(), seed=self._var_seed.get()))
        self._log_append(S['w_sep'])

        self._save_settings()

        self._q = queue.Queue()
        threading.Thread(
            target=conversion_worker,
            args=(bmd_files, folder,
                  self._var_num.get(), self._var_seed.get(),
                  self._var_hide_cmd.get(), scale_ranges,
                  self._var_select_one.get(), S, self._q,
                  self._var_hocotate_path.get().strip()),
            daemon=True
        ).start()

        self._poll()

    # ----------------------------------------------------------
    # キューのポーリング（100ms ごと）
    # ----------------------------------------------------------
    def _poll(self):
        try:
            while True:
                kind, val = self._q.get_nowait()
                if kind == MSG_LOG:
                    self._log_append(val)
                elif kind == MSG_OVERALL:
                    self._pb_overall['value'] = val
                    self._lbl_pct_overall.config(text=f'{val:3d}%')
                elif kind == MSG_FILE:
                    self._pb_file['value'] = val
                    self._lbl_pct_file.config(text=f'{val:3d}%')
                elif kind == MSG_STATUS:
                    self._lbl_status.config(text=val)
                elif kind == MSG_DONE:
                    self._running = False
                    self._btn_run.config(state='normal')
                    messagebox.showinfo(
                        self._t('dlg_done_title'), self._t('dlg_done_msg'))
                    return
                elif kind == MSG_ERROR:
                    self._running = False
                    self._btn_run.config(state='normal')
                    messagebox.showerror(self._t('dlg_err_title'), val)
                    return
        except queue.Empty:
            pass

        if self._running:
            self.after(100, self._poll)

    # ----------------------------------------------------------
    # ログ追記
    # ----------------------------------------------------------
    def _log_append(self, text):
        self._log.config(state='normal')
        self._log.insert('end', text + '\n')
        self._log.see('end')
        self._log.config(state='disabled')


# ============================================================
# エントリーポイント
# ============================================================
if __name__ == '__main__':
    app = App()
    app.mainloop()
