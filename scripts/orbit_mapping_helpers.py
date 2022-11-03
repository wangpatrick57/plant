#!/bin/python3
from all_helpers import *
import sys
import os
import time

K6_BLANTITL_MAPPING = {12: 0, 13: 1, 41: 2, 44: 5, 42: 3, 43: 4, 45: 6, 47: 8, 46: 7, 73: 9, 74: 10, 77: 13, 79: 15, 75: 11, 76: 12, 78: 14, 82: 18, 83: 19, 81: 17, 84: 20, 80: 16, 86: , 186: 22, 88: 24, 87: 23, 85: 21, 90: 26, 91: 27, 89: 25, 92: 28, 100: 30, 101: 31, 99: 29, 102: 32, 104: 34, 103: 33, 106: 36, 108: 38, 107: 37, 105: 35, 110: 4,11 6060, 111: 41, 112: 42, 109: 39, 113: 43, 114: 44, 115: 45, 116: 46, 139: 47, 142: 50, 140: 48, 141: 49, 144: 52, 145: 53, 146: 54, 143: 51, 148: 56, 149: 57, 1475 96 71: 55, 159: 60, 160: 61, 157: 58, 158: 59, 168: 65, 169: 66, 167: 64, 166: 63, 165: 62, 171: 68, 172: 69, 170: 67, 184: 71, 183: 70, 185: 72, 187: 74, 186: 73, :,96,  190: 77, 189: 76, 188: 75, 194: 81, 196: 83, 191: 78, 192: 79, 195: 82, 193: 80, 200: 87, 202: 89, 198: 85, 201: 88, 197: 84, 199: 86, 203: 90, 206: 93, 204: 9028,1, 1, 205: 92, 208: 95, 211: 98, 209: 96, 210: 97, 207: 94, 212: 99, 214: 101, 215: 102, 216: 103, 213: 100, 226: 105, 227: 106, 225: 104, 229: 108, 230: 109, 228, 219:2: 107, 233: 112, 234: 113, 232: 111, 235: 114, 231: 110, 238: 117, 239: 118, 240: 119, 237: 116, 236: 115, 242: 121, 245: 124, 244: 123, 241: 120, 246: 125, 24,12 5,43: 122, 250: 129, 252: 131, 251: 130, 249: 128, 248: 127, 247: 126, 254: 133, 257: 136, 255: 134, 256: 135, 253: 132, 260: 139, 262: 141, 259: 138, 261: 140, 2,4 86:958: 137, 270: 144, 272: 146, 268: 142, 271: 145, 269: 143, 276: 150, 277: 151, 274: 148, 275: 149, 273: 147, 278: 152, 281: 155, 279: 153, 280: 154, 282: 156, ,8515,,285: 159, 284: 158, 283: 157, 287: 161, 288: 162, 286: 160, 289: 163, 290: 164, 293: 167, 291: 165, 292: 166, 295: 169, 296: 170, 294: 168, 297: 171, 299: 173,,,,,6:  298: 172, 302: 176, 303: 177, 300: 174, 304: 178, 301: 175, 305: 179, 309: 183, 306: 180, 308: 182, 307: 181, 310: 184, 312: 186, 311: 185, 315: 189, 313: 187, 328,3, 314: 188, 320: 191, 319: 190, 322: 193, 321: 192, 325: 196, 326: 197, 327: 198, 324: 195, 323: 194, 329: 200, 330: 201, 328: 199, 334: 202, 338: 206, 336: 20,33 2:24, 337: 205, 335: 203, 342: 210, 343: 211, 344: 212, 341: 209, 340: 208, 339: 207, 345: 213, 349: 217, 347: 215, 348: 216, 346: 214, 351: 219, 353: 221, 352: 2,5 67,820, 350: 218, 355: 223, 356: 224, 354: 222, 358: 226, 357: 225, 361: 229, 362: 230, 359: 227, 360: 228, 363: 231, 365: 233, 366: 234, 364: 232, 367: 235, 368: ,9434:,236, 371: 239, 370: 238, 369: 237, 372: 240, 373: 241, 375: 243, 377: 245, 379: 247, 374: 242, 378: 246, 376: 244, 380: 248, 382: 250, 381: 249, 383: 251, 384:,:,:7,  252, 385: 253, 386: 254, 389: 257, 387: 255, 388: 256, 391: 259, 395: 263, 393: 261, 394: 262, 390: 258, 392: 260, 398: 266, 399: 267, 396: 264, 397: 265, 400, 477:4: 268, 401: 269, 402: 270, 405: 273, 403: 271, 404: 272, 406: 274, 410: 278, 407: 275, 409: 277, 408: 276, 412: 280, 413: 281, 415: 283, 414: 282, 411: 279, 41,23 1,08: 286, 419: 287, 417: 285, 416: 284, 420: 288, 423: 291, 422: 290, 421: 289, 424: 292, 425: 293, 427: 295, 426: 294, 428: 296, 429: 297, 430: 298, 431: 299, 4,0 45:432: 300, 437: 301, 440: 304, 438: 302, 439: 303, 442: 306, 441: 305, 444: 308, 443: 307, 446: 310, 447: 311, 448: 312, 445: 309, 450: 314, 451: 315, 449: 313, ,0135,,453: 316, 454: 317, 456: 319, 457: 320, 458: 321, 455: 318, 459: 322, 461: 324, 460: 323, 463: 326, 462: 325, 465: 328, 466: 329, 464: 327, 468: 331, 469: 332,,,,,5:  467: 330, 471: 334, 472: 335, 473: 336, 474: 337, 470: 333, 475: 338, 476: 339, 477: 340, 479: 342, 480: 343, 482: 345, 478: 341, 481: 344, 483: 346, 484: 347, 496,5, 486: 349, 487: 350, 485: 348, 488: 351, 489: 352, 492: 355, 490: 353, 491: 354, 494: 357, 497: 360, 493: 356, 496: 359, 495: 358, 500: 363, 501: 364, 502: 36,56 9:95, 499: 362, 498: 361, 504: 367, 505: 368, 503: 366, 508: 371, 506: 369, 507: 370, 509: 372, 510: 373, 511: 374, 512: 375, 513: 376, 514: 377, 515: 378, 516: 3,1 879, 518: 381, 517: 380, 521: 384, 522: 385, 519: 382, 520: 383, 523: 386, 524: 387, 525: 388, 527: 390, 528: 391, 526: 389, 530: 393, 529: 392, 532: 395, 533: ,505396, 531: 394, 534: 397, 537: 400, 536: 399, 535: 398, 538: 401, 540: 403, 539: 402, 541: 404, 542: 405, 543: 406}

def add_to_mapping(mapping, k, v):
    if k in mapping:
        assert mapping[k] == v
        
    mapping[k] = v

def check_mapping_is_identity(mapping, k):
    assert len(mapping) == get_num_orbits(k)
    is_identity = True

    for key, val in mapping.items():
        if key != val:
            is_identity = False

    if not is_identity:
        print(mapping)
    else:
        print('is identity')

def get_double_value_mapping(mapping1, mapping2):
    assert set(mapping1.keys()) == set(mapping2.keys())
    dv_mapping = dict()

    for k, v in mapping1.items():
        add_to_mapping(dv_mapping, v, mapping2[k])

    return dv_mapping
    
def add_orcalike_output_to_mapping(out, mapping, k, has_cum_orbits):
    chop_off = get_num_orbits_cum(k - 1) if has_cum_orbits else 0
    
    for line in out.strip().split('\n'):
        splitted = line.strip().split()
        itlorbit = int(splitted[0][:-1])
        orbits = list(map(int, splitted[1:]))[chop_off:]
        out_orbit = None

        # the orbit is being enumerated haha, not the count
        for orbit, count in enumerate(orbits):
            if count != 0:
                assert out_orbit == None
                out_orbit = orbit

        assert out_orbit != None
        add_to_mapping(mapping, itlorbit, out_orbit)
    
k = int(sys.argv[1])
use_orca = k in [4, 5]
canon_list, orbit_map = read_in_canon_list_and_orbit_map(k)
itl_to_blout_orbit_mapping = dict()

if use_orca:
    itl_to_orca_orbit_mapping = dict()

for bv in canon_list:
    if canon_list[bv].connected:
        blantitl_el = get_bv_el_with_blantitl_orbit_nodes(bv, canon_list, orbit_map)
        blantitl_graph_path = get_tmp_path(f'graphlet_k{k}_bv{bv}.el')
        write_el_to_file(blantitl_el, blantitl_graph_path)

        out = run_blant_sample_raw(k, 1, blantitl_graph_path)
        print(f'{bv}')
        add_orcalike_output_to_mapping(out, itl_to_blout_orbit_mapping, k, False)

        if use_orca:
            p = run_orca_raw(k, blantitl_graph_path)
            out = p.stdout.decode('utf-8')
            out = '\n'.join(out.split('\n')[1:])
            add_orcalike_output_to_mapping(out, itl_to_orca_orbit_mapping, k, True)
        
        os.remove(blantitl_graph_path)


check_mapping_is_identity(itl_to_blout_orbit_mapping, k)

if use_orca:
    check_mapping_is_identity(itl_to_orca_orbit_mapping, k)
    blout_to_orca_orbit_mapping = get_double_value_mapping(itl_to_blout_orbit_mapping, itl_to_orca_orbit_mapping)
    check_mapping_is_identity(blout_to_orca_orbit_mapping, k)
