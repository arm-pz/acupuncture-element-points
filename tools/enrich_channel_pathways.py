#!/usr/bin/env python3
"""Enrich data/points.json with authoritative meridian trajectories, start/end points, and total point counts."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
POINTS_JSON = ROOT / 'data' / 'points.json'

doc = json.loads(POINTS_JSON.read_text(encoding='utf-8'))

CHANNEL_INFO = {
    "LU": {
        "file": "lung-meridian-chart.html",
        "pointsCount": 11,
        "startPoint": "LU1 Zhongfu",
        "startLoc": "Anterior-lateral chest wall, 1st intercostal space, 6 cun lateral to the anterior midline",
        "endPoint": "LU11 Shaoshang",
        "endLoc": "Radial side of the thumb, 0.1 cun posterior to the corner of the nail",
        "course": "Chest → Hand (Centrifugal Yin)",
        "pathway": "Originates in the Middle Burner (stomach region), descends to connect with the Large Intestine, loops upward past the cardiac orifice, traverses the lungs, and ascends to the throat. It emerges antero-laterally at LU1 below the clavicle, runs down the antero-lateral aspect of the upper arm lateral to the biceps, crosses the cubital fossa (LU5), descends the radial forearm to the radial styloid and wrist crease (LU9), passes the thenar eminence (LU10), and terminates at the radial nail corner of the thumb at LU11. An internal branch separates at LU7 and travels directly to the radial index fingertip to connect with LI1.",
        "organs": ["Lung", "Large Intestine", "Stomach"]
    },
    "LI": {
        "file": "li-meridian-chart.html",
        "pointsCount": 20,
        "startPoint": "LI1 Shangyang",
        "startLoc": "Radial side of the index finger, 0.1 cun posterior to the corner of the nail",
        "endPoint": "LI20 Yingxiang",
        "endLoc": "In the nasolabial groove, level with the midpoint of the lateral border of the ala nasi",
        "course": "Hand → Face (Centripetal Yang)",
        "pathway": "Begins at the radial corner of the index fingernail (LI1), travels along the radial border of the index finger and across the dorsum of the hand between the 1st and 2nd metacarpals (LI4 Hegu). It ascends the lateral anterior aspect of the forearm to the lateral elbow crease (LI11 Quchi), continues up the lateral upper arm over the deltoid prominence (LI15 Jianyu), crosses posterior to the shoulder joint to the upper back (GV14 Dazhui), and enters the supraclavicular fossa (ST12). Internally, a branch descends through the lungs, penetrates the diaphragm, and enters the Large Intestine. The external branch ascends the side of the neck, crosses the cheek, enters the lower gum and teeth, curves around the lips, crosses under the philtrum (GV26) to the opposite side of the nose, and terminates at LI20 beside the contralateral nostril to connect with ST1.",
        "organs": ["Large Intestine", "Lung", "Stomach"]
    },
    "ST": {
        "file": "st-meridian-chart.html",
        "pointsCount": 45,
        "startPoint": "ST1 Chengqi",
        "startLoc": "Directly below the pupil, in the depression between the eyeball and the infraorbital ridge",
        "endPoint": "ST45 Lidui",
        "endLoc": "Lateral side of the second toe, 0.1 cun posterior to the corner of the nail",
        "course": "Face → Foot (Centrifugal Yang)",
        "pathway": "Begins beside the ala nasi (connecting from LI20), ascends to the inner canthus of the eye (BL1), then descends to the infraorbital ridge at ST1. It enters the upper gums, circles around the mouth to the chin (ST4, CV24), follows the lower jaw angle (ST6 Jiache), and ascends anterior to the ear to the coronal corner of the forehead at ST8 Touwei. A cervical branch descends from the jaw along the neck (ST9) into the supraclavicular fossa (ST12), where deep pathways plunge down through the diaphragm to enter the Stomach and connect with the Spleen. The superficial trunk branch descends across the mamillary line on the chest (4 cun lateral to midline) and abdomen (2 cun lateral to midline) down to the inguinal groove at ST30 Qichong. Continuing down the leg, it travels down the anterior thigh, over the patella and antero-lateral crest of the tibia (ST36 Zusanli), down the lower leg, over the dorsum of the foot (ST41, ST42), and terminates at the lateral nail corner of the 2nd toe at ST45. A branch from ST42 connects with SP1 on the great toe.",
        "organs": ["Stomach", "Spleen"]
    },
    "SP": {
        "file": "sp-meridian-chart.html",
        "pointsCount": 21,
        "startPoint": "SP1 Yinbai",
        "startLoc": "Medial side of the great toe, 0.1 cun posterior to the corner of the nail",
        "endPoint": "SP21 Dabao",
        "endLoc": "On the mid-axillary line, in the 7th intercostal space (or 6th in some texts)",
        "course": "Foot → Chest (Centripetal Yin)",
        "pathway": "Begins at the medial corner of the great toenail (SP1), runs along the junction of red and white skin on the medial border of the foot (SP2, SP3 Taibai), passes anterior-inferior to the medial malleolus (SP5), and ascends the postero-medial aspect of the tibia. It crosses anterior to the Liver channel at SP6 Sanyinjiao (8 cun above the malleolus), continues up the medial knee (SP9 Yinlingquan) and antero-medial thigh (SP10 Xuehai) to enter the lower abdomen at SP12. It traverses the abdomen (4 cun lateral to midline) connecting internally with the Spleen and Stomach, penetrates the diaphragm, ascends the chest (6 cun lateral to midline) to SP20, ascends the neck to spread over the lower surface of the tongue. An internal branch branches off in the chest to enter the Heart. A lateral superficial branch curves down the side of the ribcage to terminate at SP21 Dabao on the mid-axillary line as the Great Luo-connecting point of the Spleen.",
        "organs": ["Spleen", "Stomach", "Heart"]
    },
    "HT": {
        "file": "ht-meridian-chart.html",
        "pointsCount": 9,
        "startPoint": "HT1 Jiquan",
        "startLoc": "In the center of the axillary fossa, on the medial side of the axillary artery",
        "endPoint": "HT9 Shaochong",
        "endLoc": "Radial side of the little finger, 0.1 cun posterior to the corner of the nail",
        "course": "Chest → Hand (Centrifugal Yin)",
        "pathway": "Originates deep within the Heart, descends through the diaphragm to connect with the Small Intestine. An ascending internal branch travels alongside the esophagus to the eye and brain. The main somatic branch traverses the lungs and emerges in the axilla at HT1. It descends the postero-medial border of the upper arm (medial to the biceps), passes the medial end of the cubital crease at the elbow (HT3 Shaohai), descends the anterior-medial forearm along the radial side of tendon flexor carpi ulnaris to the pisiform bone and wrist crease (HT7 Shenmen). It then crosses the hypothenar eminence of the palm (HT8) and terminates at the radial nail corner of the little finger at HT9 Shaochong, connecting directly with SI1.",
        "organs": ["Heart", "Small Intestine", "Lung"]
    },
    "SI": {
        "file": "si-meridian-chart.html",
        "pointsCount": 19,
        "startPoint": "SI1 Shaoze",
        "startLoc": "Ulnar side of the little finger, 0.1 cun posterior to the corner of the nail",
        "endPoint": "SI19 Tinggong",
        "endLoc": "In the depression anterior to the tragus and posterior to the mandibular joint condyle",
        "course": "Hand → Face (Centripetal Yang)",
        "pathway": "Begins at the ulnar corner of the little fingernail (SI1), travels along the ulnar border of the hand (SI3 Houxi) and wrist (SI5), ascends the posterior-ulnar border of the forearm, and passes between the olecranon process and medial epicondyle of the humerus at the elbow (SI8 Xiaohai). It ascends the posterior upper arm to the shoulder joint, zig-zags across the infraspinous and supraspinous fossae of the scapula (SI9-SI13), meets the midline at the lower cervical spine (GV14 Dazhui), and curves forward over the shoulder into the supraclavicular fossa (ST12). An internal branch plunges downward to connect with the Heart, descends through the diaphragm to the Stomach, and enters the Small Intestine. The ascending superficial branch rises along the lateral neck (SI16, SI17), crosses the cheek to the outer canthus of the eye (linking to BL1), and enters the auditory canal, terminating in front of the tragus at SI19 Tinggong.",
        "organs": ["Small Intestine", "Heart", "Stomach"]
    },
    "BL": {
        "file": "bl-meridian-chart.html",
        "pointsCount": 67,
        "startPoint": "BL1 Jingming",
        "startLoc": "In the depression 0.1 cun superior to the inner canthus of the eye",
        "endPoint": "BL67 Zhiyin",
        "endLoc": "Lateral side of the fifth (little) toe, 0.1 cun posterior to the corner of the nail",
        "course": "Face → Foot (Centrifugal Yang)",
        "pathway": "The longest channel in the human body (67 points). Originates at the inner canthus of the eye (BL1), ascends over the forehead to the vertex (BL7, GV20), enters the brain, emerges at the occiput, and descends to the nape of the neck at BL10 Tianzhu. From the neck, it divides into two bilateral descending tracks down the dorsal spine: the inner line (1.5 cun lateral to midline, BL11 to BL30 carrying the Back-Shu points) which descends into the lumbar area to enter the Kidneys and Bladder, continuing over the sacrum to the popliteal fossa (BL40 Weizhong); and the outer line (3.0 cun lateral to midline, BL41 to BL54) which descends through the scapular border, gluteal region, and posterior thigh to reunite with the inner line at BL40. The reunited channel descends down the middle of the posterior calf (BL57), curves behind the lateral malleolus (BL60 Kunlun), travels along the lateral margin of the foot (BL65), and terminates at the lateral nail corner of the little toe at BL67 Zhiyin, linking directly with KI1.",
        "organs": ["Bladder", "Kidney", "Brain"]
    },
    "KI": {
        "file": "ki-meridian-chart.html",
        "pointsCount": 27,
        "startPoint": "KI1 Yongquan",
        "startLoc": "On the sole of the foot, between the 2nd and 3rd metatarsal bones, one-third of the distance from the web space to the heel",
        "endPoint": "KI27 Shufu",
        "endLoc": "In the depression on the lower border of the clavicle, 2 cun lateral to the anterior midline",
        "course": "Foot → Chest (Centripetal Yin)",
        "pathway": "Originates on the plantar surface beneath the little toe, traverses diagonally across the sole of the foot to emerge at KI1 Yongquan. It passes under the tuberosity of the navicular bone (KI2), loops behind and inferior to the medial malleolus (KI3 Taixi), encircles the heel, ascends the postero-medial aspect of the lower leg (KI7 Fuliu), and reaches the medial side of the popliteal crease (KI10 Yingu). Ascending the posterior-medial thigh to the base of the spine, it enters the Kidney and connects with the Urinary Bladder. Emerging at the lower abdomen 0.5 cun lateral to the midline (KI11-KI16), it ascends through the abdomen and diaphragm, continuing up the chest 2 cun lateral to the midline (KI21-KI27), terminating just below the clavicle at KI27 Shufu. Deep branches ascend through the Liver, Lungs, and throat to terminate at the root of the tongue.",
        "organs": ["Kidney", "Bladder", "Liver", "Lung", "Heart"]
    },
    "PC": {
        "file": "pc-meridian-chart.html",
        "pointsCount": 9,
        "startPoint": "PC1 Tianchi",
        "startLoc": "In the 4th intercostal space, 1 cun lateral to the nipple, 5 cun lateral to the anterior midline",
        "endPoint": "PC9 Zhongchong",
        "endLoc": "At the center of the tip of the middle finger (or 0.1 cun from the radial nail corner)",
        "course": "Chest → Hand (Centrifugal Yin)",
        "pathway": "Originates deep inside the chest in the pericardium, descends through the diaphragm into the abdomen to connect with the upper, middle, and lower burners (San Jiao). A lateral chest branch emerges at PC1 (1 cun lateral to the nipple), arches over the axilla, and travels down the antero-medial aspect of the upper arm between the two heads of the biceps brachii. It crosses the cubital fossa medial to the biceps tendon (PC3 Quze), runs down the midline of the anterior forearm between the tendons of palmaris longus and flexor carpi radialis (passing PC5, PC6 Neiguan, and PC7 Daling at the wrist crease), traverses the center of the palm (PC8 Laogong), and terminates at the tip of the middle finger at PC9 Zhongchong. A collateral branch separates at PC8 and travels to the ulnar tip of the ring finger to connect with TB1.",
        "organs": ["Pericardium", "Triple Burner (San Jiao)"]
    },
    "TB": {
        "file": "tb-meridian-chart.html",
        "pointsCount": 23,
        "startPoint": "TB1 Guanchong",
        "startLoc": "Ulnar side of the ring finger, 0.1 cun posterior to the corner of the nail",
        "endPoint": "TB23 Sizhukong",
        "endLoc": "In the depression at the lateral end of the eyebrow",
        "course": "Hand → Face (Centripetal Yang)",
        "pathway": "Begins at the ulnar nail corner of the ring finger (TB1), traverses the dorsum of the hand between the 4th and 5th metacarpal bones (TB3 Zhongzhu), over the dorsal wrist crease (TB4 Yangchi), and ascends the dorsal midline of the forearm between the radius and ulna (TB5 Waiguan, TB6 Zhigou). It passes the tip of the olecranon at the elbow (TB10 Tianjing), ascends the posterior upper arm to the shoulder (TB14), crosses the trapezial ridge (TB15), meets GV14 at the spine, and enters the supraclavicular fossa (ST12). Internally, it descends into the chest, connects with the Pericardium, and penetrates the diaphragm to link the Upper, Middle, and Lower Burners (San Jiao). The ascending superficial branch rises along the neck to the posterior base of the ear (TB17 Yifeng), curves around the posterior and superior rim of the ear, enters the ear, emerges anterior to the ear, crosses the cheek, and terminates in the depression at the lateral tip of the eyebrow at TB23 Sizhukong, linking with GB1 at the outer eye canthus.",
        "organs": ["Triple Burner (San Jiao)", "Pericardium"]
    },
    "GB": {
        "file": "gb-meridian-chart.html",
        "pointsCount": 44,
        "startPoint": "GB1 Tongziliao",
        "startLoc": "In the depression 0.5 cun lateral to the outer canthus of the eye",
        "endPoint": "GB44 Zuqiaoyin",
        "endLoc": "Lateral side of the 4th toe, 0.1 cun posterior to the corner of the nail",
        "course": "Face → Foot (Centrifugal Yang)",
        "pathway": "Begins at the outer canthus of the eye (GB1), ascends to the temporal hairline, zig-zags across the temporal region, loops behind the ear to the occiput at GB20 Fengchi, curves back over the scalp to the forehead above the pupil (GB14), then sweeps back over the head to the crest of the shoulder (GB21 Jianjing). It enters the supraclavicular fossa (ST12), where internal branches descend through the chest to connect with the Liver and Gallbladder. The external branch descends down the lateral axillary line and ribcage (GB24, GB25), loops across the pelvis to the greater trochanter of the femur (GB30 Huantiao). It descends the lateral aspect of the thigh and knee, down the anterior margin of the fibula (GB34 Yanglingquan), passes anterior-inferior to the lateral malleolus (GB40 Qiuxu), traverses the dorsum of the foot between the 4th and 5th metatarsals (GB41 Zulinqi), and terminates at the lateral nail corner of the 4th toe at GB44 Zuqiaoyin. An internal foot branch separates at GB41 and runs to the great toe to link with LR1.",
        "organs": ["Gallbladder", "Liver"]
    },
    "LR": {
        "file": "lr-meridian-chart.html",
        "pointsCount": 14,
        "startPoint": "LR1 Dadun",
        "startLoc": "Lateral side of the great toe, 0.1 cun posterior to the corner of the nail",
        "endPoint": "LR14 Qimen",
        "endLoc": "In the 6th intercostal space, on the mamillary line, 4 cun lateral to the anterior midline",
        "course": "Foot → Chest (Centripetal Yin)",
        "pathway": "Begins at the lateral/dorsal nail corner of the great toe (LR1), ascends the dorsum of the foot between the 1st and 2nd metatarsals (LR2, LR3 Taichong), passes 1 cun anterior to the medial malleolus (LR4 Zhongfeng), and ascends the medial lower leg along the medial border of the tibia. It crosses 8 cun above the medial malleolus behind the Spleen channel, passes the medial aspect of the knee crease (LR8 Ququan), and ascends the medial thigh to the groin. It encircles the external genitalia, enters the lower abdomen, ascends parallel to the Stomach channel, and connects internally with the Liver and Gallbladder. Penetrating the diaphragm, it spreads across the costal and hypochondriac region, terminating superficially at the 6th intercostal space at LR14 Qimen. An internal branch ascends along the esophagus and posterior pharynx to connect with the eye tissues, forehead, and vertex at GV20 Baihui. Another internal branch separates from the liver, crosses the diaphragm, and enters the lungs to connect with LU1, completing the continuous 12-channel cycle.",
        "organs": ["Liver", "Gallbladder", "Lung", "Stomach"]
    }
}

for c in doc['channels']:
    info = CHANNEL_INFO[c['abbr']]
    c['file'] = info['file']
    c['pointsCount'] = info['pointsCount']
    c['startPoint'] = info['startPoint']
    c['startLoc'] = info['startLoc']
    c['endPoint'] = info['endPoint']
    c['endLoc'] = info['endLoc']
    c['course'] = info['course']
    c['pathway'] = info['pathway']
    c['organs'] = info['organs']

POINTS_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print("Successfully enriched data/points.json with all 12 channel trajectories and point counts!")
