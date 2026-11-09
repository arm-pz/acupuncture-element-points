#!/usr/bin/env python3
"""Build high-effort, beautiful, transit-atlas grade meridian pathway banners for all 12 channels."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
POINTS_JSON = ROOT / 'data' / 'points.json'

doc = json.loads(POINTS_JSON.read_text(encoding='utf-8'))

CHANNEL_DETAILS = {
    "LU": {
        "start": {
            "code": "LU1",
            "py": "Zhongfu",
            "hz": "中府",
            "en": "Central Treasury",
            "landmark": "Anterior Chest Wall · 1st Intercostal Space",
            "loc": "In the 1st intercostal space, 6 cun lateral to the anterior midline, below the clavicle."
        },
        "end": {
            "code": "LU11",
            "py": "Shaoshang",
            "hz": "少商",
            "en": "Lesser Shang",
            "landmark": "Radial Nail Angle · Thumb",
            "loc": "On the radial side of the thumb, 0.1 cun posterior to the corner of the nail.",
            "handoff": "Collateral separates at LU7 to connect with LI1 (Index Finger)"
        },
        "course": "Chest → Hand (Centrifugal Yin)",
        "tide": "03:00 – 05:00 · Yin Hour (寅時)",
        "organs": {
            "primary": "Lung (肺 · Zang)",
            "paired": "Large Intestine (大腸 · Fu)",
            "tissues": "Skin · Body Hair · Throat · Nasal Passages"
        },
        "stages": [
            {
                "num": "01",
                "title": "Middle Burner Internal Genesis",
                "desc": "Originates internally in the Middle Burner (stomach region), descends to connect with and encircle the Large Intestine, turns back upward to skirt the cardiac orifice of the stomach, traverses the diaphragm, and enters the Lungs (its primary Zang organ)."
            },
            {
                "num": "02",
                "title": "Respiratory Trunk & Axillary Emergence",
                "desc": "Ascends the respiratory tract to the larynx and throat, then sweeps laterally to erupt superficially on the antero-lateral chest wall at LU1 Zhongfu (1st intercostal space), ascending to LU2 Yunmen directly below the clavicle."
            },
            {
                "num": "03",
                "title": "Brachial Descent & Cubital Traversal",
                "desc": "Arches over the axilla, descends the antero-lateral border of the upper arm lateral to the biceps tendon, passes the cubital crease at LU5 Chize (He-Sea), and proceeds down the radial margin of the anterior forearm along the brachioradialis muscle."
            },
            {
                "num": "04",
                "title": "Styloid Wrist, Thenar Eminence & Acral Terminus",
                "desc": "Traverses the radial styloid process at LU7 Lieque, crosses the wrist crease at LU9 Taiyuan (Yuan-Source), sweeps across the fleshy thenar eminence at LU10 Yuji, and terminates at the radial nail corner of the thumb at LU11 Shaoshang (Jing-Well). An internal branch divides at LU7 Lieque to meet LI1 Shangyang on the index finger."
            }
        ]
    },
    "LI": {
        "start": {
            "code": "LI1",
            "py": "Shangyang",
            "hz": "商陽",
            "en": "Shang Yang",
            "landmark": "Radial Nail Angle · Index Finger",
            "loc": "On the radial side of the index finger, 0.1 cun posterior to the corner of the nail."
        },
        "end": {
            "code": "LI20",
            "py": "Yingxiang",
            "hz": "迎香",
            "en": "Welcome Fragrance",
            "landmark": "Nasolabial Groove · Ala Nasi",
            "loc": "In the nasolabial groove, level with the midpoint of the lateral border of the ala nasi.",
            "handoff": "Internal link meets ST1 Chengqi at the infraorbital ridge"
        },
        "course": "Hand → Face (Centripetal Yang)",
        "tide": "05:00 – 07:00 · Mao Hour (卯時)",
        "organs": {
            "primary": "Large Intestine (大腸 · Fu)",
            "paired": "Lung (肺 · Zang)",
            "tissues": "Large Intestine · Mucous Membranes · Teeth · Lower Gums"
        },
        "stages": [
            {
                "num": "01",
                "title": "Digital Ascent & Metacarpal Web",
                "desc": "Commences at the radial nail angle of the index finger at LI1 Shangyang, ascends the radial margin of the finger across the 1st and 2nd metacarpal interspace at LI4 Hegu, and passes the anatomical snuffbox into the posterior-radial forearm."
            },
            {
                "num": "02",
                "title": "Lateral Forearm, Elbow Crease & Shoulder",
                "desc": "Courses up the lateral radial border of the forearm between the extensor muscles, reaches the lateral elbow crease at LI11 Quchi, ascends the lateral arm over the deltoid insertion to the shoulder prominence at LI15 Jianyu, and converges at the spine at GV14 Dazhui."
            },
            {
                "num": "03",
                "title": "Supraclavicular Entry & Visceral Plunge",
                "desc": "Arches over the shoulder into the supraclavicular fossa at ST12 Quepen; deep internal vessels plunge into the chest through the Lungs, penetrate the diaphragm, and enter the Large Intestine to regulate fluid absorption."
            },
            {
                "num": "04",
                "title": "Cervical Ascent, Oral Decussation & Nostril Terminus",
                "desc": "The superficial branch ascends the lateral neck through the sternocleidomastoid muscle, traverses the mandible, enters the lower gums and lower teeth, encircles the lips, decussates (crosses over) under the philtrum at GV26, and terminates beside the opposite nostril at LI20 Yingxiang to meet ST1."
            }
        ]
    },
    "ST": {
        "start": {
            "code": "ST1",
            "py": "Chengqi",
            "hz": "承泣",
            "en": "Container of Tears",
            "landmark": "Infraorbital Ridge · Eye Orbit",
            "loc": "Directly below the pupil, in the depression between the eyeball and the infraorbital ridge."
        },
        "end": {
            "code": "ST45",
            "py": "Lidui",
            "hz": "厲兌",
            "en": "Strict Exchange",
            "landmark": "Lateral Nail Angle · 2nd Toe",
            "loc": "Lateral side of the second toe, 0.1 cun posterior to the corner of the nail.",
            "handoff": "Dorsal foot branch at ST42 connects with SP1 Yinbai (Great Toe)"
        },
        "course": "Face → Foot (Centrifugal Yang)",
        "tide": "07:00 – 09:00 · Chen Hour (辰時)",
        "organs": {
            "primary": "Stomach (胃 · Fu)",
            "paired": "Spleen (脾 · Zang)",
            "tissues": "Muscles · Mouth · Upper Teeth · Gums · Breast · Flesh"
        },
        "stages": [
            {
                "num": "01",
                "title": "Craniofacial Circuit & Mandibular Arch",
                "desc": "Originates at the lateral nostril, ascends to the inner eye canthus (BL1), drops to the infraorbital ridge at ST1 Chengqi, enters upper gums, circles around the mouth to the chin groove, sweeps across the jaw angle at ST6 Jiache, and climbs anterior to the ear to the coronal skull at ST8 Touwei."
            },
            {
                "num": "02",
                "title": "Cervical Drop, Thoracic Mamillary Line & Abdomen",
                "desc": "Descends along the carotid sheath (ST9 Renying) into the supraclavicular fossa (ST12). Deep internal branches penetrate the diaphragm to enter the Stomach and connect with the Spleen. The external trunk descends 4 cun lateral to the midline on the chest and 2 cun on the abdomen down to ST30 Qichong at the groin."
            },
            {
                "num": "03",
                "title": "Femoral Descent, Patella & Tibial Crest",
                "desc": "Emerges at the inguinal crease, descends the anterior thigh along the rectus femoris muscle, crosses the patella into the lateral lower leg alongside the anterior tibial crest through ST36 Zusanli, and continues down the tibialis anterior muscle."
            },
            {
                "num": "04",
                "title": "Dorsum of Foot to Second Toe Terminus",
                "desc": "Crosses the ankle joint and dorsum of the foot between the 2nd and 3rd metatarsals (ST41, ST42), terminating at the lateral nail corner of the 2nd toe at ST45 Lidui. A collateral separates at ST42 Chongyang and travels to the medial tip of the great toe to join SP1 Yinbai."
            }
        ]
    },
    "SP": {
        "start": {
            "code": "SP1",
            "py": "Yinbai",
            "hz": "隱白",
            "en": "Hidden White",
            "landmark": "Medial Nail Angle · Great Toe",
            "loc": "On the medial side of the great toe, 0.1 cun posterior to the corner of the nail."
        },
        "end": {
            "code": "SP21",
            "py": "Dabao",
            "hz": "大包",
            "en": "Great Enfolding",
            "landmark": "7th Intercostal Space · Mid-Axillary Line",
            "loc": "On the mid-axillary line, in the 7th intercostal space.",
            "handoff": "Internal chest branch disperses into the Heart"
        },
        "course": "Foot → Chest (Centripetal Yin)",
        "tide": "09:00 – 11:00 · Si Hour (巳時)",
        "organs": {
            "primary": "Spleen (脾 · Zang)",
            "paired": "Stomach (胃 · Fu)",
            "tissues": "Muscles · Flesh · Lips · Connective Tissues · Blood Vessels"
        },
        "stages": [
            {
                "num": "01",
                "title": "Medial Pedal Border & Malleolar Bypass",
                "desc": "Begins at the medial nail angle of the great toe at SP1 Yinbai, courses along the junction of red and white skin past the 1st metatarsophalangeal joint at SP3 Taibai, and sweeps anterior and superior to the medial malleolus at SP5 Shangqiu."
            },
            {
                "num": "02",
                "title": "Tibial Cruciate Crossing & Medial Knee",
                "desc": "Climbs the posterior-medial border of the tibia, crosses anterior to the Liver channel at SP6 Sanyinjiao (8 cun above the malleolus), passes the medial condyle of the tibia at SP9 Yinlingquan, and ascends the antero-medial thigh through SP10 Xuehai to the groin."
            },
            {
                "num": "03",
                "title": "Abdominal Route, Visceral Union & Lingual Root",
                "desc": "Enters the lower abdomen at SP12, traverses 4 cun lateral to the midline connecting internally with the Spleen and Stomach, ascends through the diaphragm and chest (6 cun lateral) to SP20, and rises along the esophagus to disperse under the lower surface of the tongue."
            },
            {
                "num": "04",
                "title": "Cardio-Visceral Link & Great Luo (Dabao)",
                "desc": "An internal branch departs the chest to enter the Heart. The superficial pathway sweeps downward and laterally across the side of the ribcage to terminate at SP21 Dabao in the 7th intercostal space, reigning as the Great Luo-connecting point over all collateral vessels."
            }
        ]
    },
    "HT": {
        "start": {
            "code": "HT1",
            "py": "Jiquan",
            "hz": "極泉",
            "en": "Highest Spring",
            "landmark": "Axillary Fossa Apex · Axillary Artery",
            "loc": "In the center of the axillary fossa, on the medial side of the axillary artery."
        },
        "end": {
            "code": "HT9",
            "py": "Shaochong",
            "hz": "少衝",
            "en": "Lesser Surge",
            "landmark": "Radial Nail Angle · Little Finger",
            "loc": "Radial side of the little finger, 0.1 cun posterior to the corner of the nail.",
            "handoff": "Immediate surface link to SI1 Shaoze at little finger"
        },
        "course": "Chest → Hand (Centrifugal Yin)",
        "tide": "11:00 – 13:00 · Wu Hour (午時)",
        "organs": {
            "primary": "Heart (心 · Zang)",
            "paired": "Small Intestine (小腸 · Fu)",
            "tissues": "Blood Vessels · Tongue · Complexion · Shen (Mind)"
        },
        "stages": [
            {
                "num": "01",
                "title": "Cardiocentric Origin & Deep Visceral Branches",
                "desc": "Originates deep within the Heart, descends through the diaphragm to communicate with the Small Intestine; an ascending visceral branch travels up alongside the esophagus to connect with the ocular system, optic nerve, and brain."
            },
            {
                "num": "02",
                "title": "Pulmonary Traversal & Axillary Emergence",
                "desc": "The main superficial trunk travels across the lung tissues and bursts forth in the center of the armpit at HT1 Jiquan, descending along the postero-medial aspect of the upper arm medial to the biceps muscle."
            },
            {
                "num": "03",
                "title": "Cubital Crease to Pisiform Bone",
                "desc": "Passes the medial epicondyle of the humerus at HT3 Shaohai, descends the anterior-medial forearm along the radial side of the flexor carpi ulnaris tendon, and reaches the pisiform bone and wrist crease at HT7 Shenmen (Yuan-Source)."
            },
            {
                "num": "04",
                "title": "Hypothenar Palm to Little Fingertip",
                "desc": "Crosses the hypothenar eminence between the 4th and 5th metacarpal bones at HT8 Shaofu, and terminates at the radial nail corner of the little finger at HT9 Shaochong (Jing-Well), linking directly with SI1 Shaoze on the ulnar side."
            }
        ]
    },
    "SI": {
        "start": {
            "code": "SI1",
            "py": "Shaoze",
            "hz": "少澤",
            "en": "Lesser Marsh",
            "landmark": "Ulnar Nail Angle · Little Finger",
            "loc": "On the ulnar side of the little finger, 0.1 cun posterior to the corner of the nail."
        },
        "end": {
            "code": "SI19",
            "py": "Tinggong",
            "hz": "聽宮",
            "en": "Palace of Hearing",
            "landmark": "Preauricular Depression · Tragus",
            "loc": "In the depression anterior to the tragus and posterior to the mandibular condyle.",
            "handoff": "Facial branch links with BL1 Jingming at inner canthus"
        },
        "course": "Hand → Face (Centripetal Yang)",
        "tide": "13:00 – 15:00 · Wei Hour (未時)",
        "organs": {
            "primary": "Small Intestine (小腸 · Fu)",
            "paired": "Heart (心 · Zang)",
            "tissues": "Ears · Scapular Region · Upper Back · Lower Abdomen"
        },
        "stages": [
            {
                "num": "01",
                "title": "Digital Ulnar Ascent & Metacarpal Border",
                "desc": "Begins at the ulnar nail angle of the little finger at SI1 Shaoze, courses along the ulnar margin of the hand past the 5th metacarpal head at SI3 Houxi, crosses the ulnar wrist crease at SI5 Yanggu, and climbs the posterior ulnar crest of the forearm."
            },
            {
                "num": "02",
                "title": "Olecranon Groove to Scapular Traversal",
                "desc": "Passes between the olecranon tip and medial epicondyle of the humerus at SI8 Xiaohai, ascends the posterior triceps to the shoulder joint, and zig-zags across the infraspinous and supraspinous fossae of the scapula (SI9–SI13)."
            },
            {
                "num": "03",
                "title": "Spinal Union & Visceral Penetration",
                "desc": "Reaches the midline at the 7th cervical vertebra (GV14 Dazhui), arches forward into the supraclavicular fossa (ST12), and sends deep vessels down through the Heart, diaphragm, and Stomach to enter the Small Intestine."
            },
            {
                "num": "04",
                "title": "Cervical Ascent, Zygoma & Preauricular Tragus",
                "desc": "The external ascending branch climbs the lateral neck, crosses the cheekbone, divides to send an internal link to the inner eye canthus (BL1), and enters the auditory canal, terminating directly in front of the tragus at SI19 Tinggong."
            }
        ]
    },
    "BL": {
        "start": {
            "code": "BL1",
            "py": "Jingming",
            "hz": "睛明",
            "en": "Bright Eyes",
            "landmark": "Inner Canthus · Nasal Bridge",
            "loc": "In the depression 0.1 cun superior to the inner canthus of the eye."
        },
        "end": {
            "code": "BL67",
            "py": "Zhiyin",
            "hz": "至陰",
            "en": "Reaching Yin",
            "landmark": "Lateral Nail Angle · 5th Toe",
            "loc": "Lateral side of the fifth (little) toe, 0.1 cun posterior to the corner of the nail.",
            "handoff": "Internal plantar branch links with KI1 Yongquan in the sole"
        },
        "course": "Face → Foot (Centrifugal Yang)",
        "tide": "15:00 – 17:00 · Shen Hour (申時)",
        "organs": {
            "primary": "Bladder (膀胱 · Fu)",
            "paired": "Kidney (腎 · Zang)",
            "tissues": "Bones · Brain · Spinal Cord · Eyes · Dorsal Axial Muscles"
        },
        "stages": [
            {
                "num": "01",
                "title": "Canthal Origin, Vertex Crown & Brain Entry",
                "desc": "Originates at the inner eye canthus at BL1 Jingming, crosses the forehead to the vertex (BL7, GV20), enters the brain to communicate with cerebral marrow, and emerges at the occiput to descend to the nape of the neck at BL10 Tianzhu."
            },
            {
                "num": "02",
                "title": "Dual Bilateral Paravertebral Columns",
                "desc": "Bifurcates at the neck into two parallel descending spinal columns: the Inner Line (1.5 cun lateral, housing all Back-Shu points BL11–BL30 which penetrate Kidneys and Bladder) and the Outer Line (3.0 cun lateral, BL41–BL54), both converging at the popliteal crease at BL40 Weizhong."
            },
            {
                "num": "03",
                "title": "Gastrocnemius Calf Descent to Lateral Malleolus",
                "desc": "The reunited channel descends down the dorsal midline of the calf bellies through BL57 Chengshan, emerges lateral to the Achilles tendon, and winds behind the prominence of the lateral malleolus at BL60 Kunlun."
            },
            {
                "num": "04",
                "title": "Lateral Foot Margin to Fifth Toe Terminus",
                "desc": "Courses along the lateral border of the foot past the tuberosity of the 5th metatarsal at BL65 Shugu, terminating at the lateral nail corner of the little toe at BL67 Zhiyin. A collateral branch dives into the plantar sole to link with KI1 Yongquan."
            }
        ]
    },
    "KI": {
        "start": {
            "code": "KI1",
            "py": "Yongquan",
            "hz": "湧泉",
            "en": "Gushing Spring",
            "landmark": "Plantar Sole · Metatarsal Web Space",
            "loc": "On the sole of the foot, between the 2nd and 3rd metatarsal heads, 1/3 distance from web to heel."
        },
        "end": {
            "code": "KI27",
            "py": "Shufu",
            "hz": "俞府",
            "en": "Shu Mansion",
            "landmark": "Infraclavicular Depression · 2 Cun Lateral",
            "loc": "In the depression on the lower border of the clavicle, 2 cun lateral to the anterior midline.",
            "handoff": "Internal chest branch disperses into the Heart and Pericardium"
        },
        "course": "Foot → Chest (Centripetal Yin)",
        "tide": "17:00 – 19:00 · You Hour (酉時)",
        "organs": {
            "primary": "Kidney (腎 · Zang)",
            "paired": "Bladder (膀胱 · Fu)",
            "tissues": "Bones · Marrow · Ears · Teeth · Lumbar Spine · Hair"
        },
        "stages": [
            {
                "num": "01",
                "title": "Plantar Genesis & Retrograde Malleolar Loop",
                "desc": "Begins on the plantar surface beneath the 5th toe, traverses diagonally across the sole to erupt at KI1 Yongquan, crosses the navicular tuberosity, and loops in a complete retrograde circle behind and below the medial malleolus at KI3 Taixi."
            },
            {
                "num": "02",
                "title": "Calcaneal Loop & Postero-Medial Popliteal Crease",
                "desc": "Encircles the heel, ascends the postero-medial lower leg anterior to the Achilles tendon (KI7 Fuliu), reaches the medial end of the popliteal crease at KI10 Yingu, and ascends the medial thigh to the base of the spine at the coccyx."
            },
            {
                "num": "03",
                "title": "Abdominal & Thoracic Paramedian Ascent",
                "desc": "Penetrates the Kidneys and Bladder; emerges on the lower abdomen 0.5 cun lateral to midline (KI11–KI16), ascends through the diaphragm, and continues up the chest 2 cun lateral to midline (KI21–KI27), terminating under the clavicle at KI27 Shufu."
            },
            {
                "num": "04",
                "title": "Hepato-Pulmonary Vessels & Lingual Root",
                "desc": "Deep internal collaterals ascend through the Liver and Lungs, travel along the throat, and terminate at the root of the tongue, while an internal branch disperses from the chest into the Heart to link with the Pericardium channel."
            }
        ]
    },
    "PC": {
        "start": {
            "code": "PC1",
            "py": "Tianchi",
            "hz": "天池",
            "en": "Heavenly Pool",
            "landmark": "4th Intercostal Space · 1 Cun Lateral to Nipple",
            "loc": "In the 4th intercostal space, 1 cun lateral to the nipple, 5 cun lateral to the anterior midline."
        },
        "end": {
            "code": "PC9",
            "py": "Zhongchong",
            "hz": "中衝",
            "en": "Middle Surge",
            "landmark": "Tip of Middle Finger · Apex",
            "loc": "At the center of the tip of the middle finger (or 0.1 cun from radial nail corner).",
            "handoff": "Collateral from PC8 Laogong travels to TB1 Guanchong (Ring Finger)"
        },
        "course": "Chest → Hand (Centrifugal Yin)",
        "tide": "19:00 – 21:00 · Xu Hour (戌時)",
        "organs": {
            "primary": "Pericardium (心包 · Zang)",
            "paired": "Triple Burner (三焦 · Fu)",
            "tissues": "Blood Vessels · Chest · Heart Envelope · Mind/Shen"
        },
        "stages": [
            {
                "num": "01",
                "title": "Cardio-Pericardial Origin & Three Burners",
                "desc": "Originates deep inside the chest within the pericardium, plunges through the diaphragm into the abdomen, systematically connecting and harmonizing the Upper, Middle, and Lower Burners (San Jiao)."
            },
            {
                "num": "02",
                "title": "Lateral Pectoral Emergence & Bicipital Arm",
                "desc": "A chest branch emerges 1 cun lateral to the nipple at PC1 Tianchi, arches over the axilla, and travels down the antero-medial aspect of the arm between the two heads of the biceps brachii muscle."
            },
            {
                "num": "03",
                "title": "Cubital Fossa to Inter-Tendinous Forearm",
                "desc": "Crosses the cubital fossa medial to the biceps tendon at PC3 Quze, descends the exact midline of the forearm between the tendons of palmaris longus and flexor carpi radialis through PC6 Neiguan, and reaches the wrist crease at PC7 Daling."
            },
            {
                "num": "04",
                "title": "Palmar Center to Middle Fingertip",
                "desc": "Crosses the center of the palm between the 2nd and 3rd metacarpals at PC8 Laogong, and terminates at the central tip of the middle finger at PC9 Zhongchong. An internal branch separates at PC8 to link with TB1 Guanchong on the ring finger."
            }
        ]
    },
    "TB": {
        "start": {
            "code": "TB1",
            "py": "Guanchong",
            "hz": "關衝",
            "en": "Rushing Pass",
            "landmark": "Ulnar Nail Angle · Ring Finger",
            "loc": "On the ulnar side of the ring finger, 0.1 cun posterior to the corner of the nail."
        },
        "end": {
            "code": "TB23",
            "py": "Sizhukong",
            "hz": "絲竹空",
            "en": "Silken Bamboo Hollow",
            "landmark": "Lateral Eyebrow End · Temporal Depression",
            "loc": "In the depression at the lateral end of the eyebrow.",
            "handoff": "Superficial facial branch links with GB1 Tongziliao at outer canthus"
        },
        "course": "Hand → Face (Centripetal Yang)",
        "tide": "21:00 – 23:00 · Hai Hour (亥時)",
        "organs": {
            "primary": "Triple Burner (三焦 · Fu)",
            "paired": "Pericardium (心包 · Zang)",
            "tissues": "Water Metabolism · Fluid Passages · Lymphatics · Ears · Temples"
        },
        "stages": [
            {
                "num": "01",
                "title": "Digital Ulnar Genesis & Dorsal Hand",
                "desc": "Commences at the ulnar nail angle of the ring finger at TB1 Guanchong, courses along the dorsum of the hand between the 4th and 5th metacarpals through TB3 Zhongzhu, over the dorsal wrist crease (TB4), and up the interosseous space of the forearm between radius and ulna (TB5, TB6)."
            },
            {
                "num": "02",
                "title": "Olecranon Tip, Posterior Triceps & Shoulder",
                "desc": "Climbs past the olecranon tip at TB10 Tianjing, ascends the posterior triceps surface to the shoulder at TB14, sweeps across the trapezius ridge (TB15), and converges at the spine at GV14 Dazhui."
            },
            {
                "num": "03",
                "title": "Supraclavicular Entry & San Jiao Visceral Drop",
                "desc": "Enters the supraclavicular fossa (ST12), dives into the chest to connect with the Pericardium, and penetrates the diaphragm to link and coordinate the Upper, Middle, and Lower Burners (San Jiao)."
            },
            {
                "num": "04",
                "title": "Auricular Circumference to Eyebrow Tip",
                "desc": "The cervical branch ascends the side of the neck to retro-auricular TB17 Yifeng, loops around the ear helix into the auditory canal, re-emerges anterior to the ear, and terminates in the depression at the lateral end of the eyebrow at TB23 Sizhukong to meet GB1."
            }
        ]
    },
    "GB": {
        "start": {
            "code": "GB1",
            "py": "Tongziliao",
            "hz": "瞳子髎",
            "en": "Pupil Bone Hole",
            "landmark": "Outer Canthus · Lateral Orbital Rim",
            "loc": "In the depression 0.5 cun lateral to the outer canthus of the eye."
        },
        "end": {
            "code": "GB44",
            "py": "Zuqiaoyin",
            "hz": "足竅陰",
            "en": "Foot Portal Yin",
            "landmark": "Lateral Nail Angle · 4th Toe",
            "loc": "Lateral side of the fourth toe, 0.1 cun posterior to the corner of the nail.",
            "handoff": "Internal foot branch leaves GB41 to connect with LR1 Dadun (Great Toe)"
        },
        "course": "Face → Foot (Centrifugal Yang)",
        "tide": "23:00 – 01:00 · Zi Hour (子時)",
        "organs": {
            "primary": "Gallbladder (膽 · Fu)",
            "paired": "Liver (肝 · Zang)",
            "tissues": "Tendons · Sinews · Eyes · Temporal Region · Hips · Flanks"
        },
        "stages": [
            {
                "num": "01",
                "title": "Cranial Triple-Loop & Suboccipital Base",
                "desc": "Originates at the outer eye canthus at GB1 Tongziliao, ascends to the temporal hairline, zig-zags across the temple, loops behind the ear to the suboccipital skull at GB20 Fengchi, curves back over the frontal scalp above the pupil (GB14), and sweeps over the shoulder crest at GB21 Jianjing."
            },
            {
                "num": "02",
                "title": "Supraclavicular Entry, Lateral Ribcage & Hip Joint",
                "desc": "Dips into the supraclavicular fossa (ST12) sending deep vessels to link with Liver and Gallbladder; the superficial branch descends the mid-axillary line, zig-zags across the hypochondriac ribs (GB24, GB25), and loops over the greater trochanter at GB30 Huantiao."
            },
            {
                "num": "03",
                "title": "Lateral Thigh, Fibular Crest & Lateral Malleolus",
                "desc": "Descends the iliotibial band of the lateral thigh, crosses the lateral knee crease, runs down the anterior margin of the fibula through GB34 Yanglingquan, and passes anterior-inferior to the lateral malleolus at GB40 Qiuxu."
            },
            {
                "num": "04",
                "title": "4th Metatarsal Interspace to 4th Toe Terminus",
                "desc": "Traverses the dorsum of the foot between the 4th and 5th metatarsal bones at GB41 Zulinqi, terminating at the lateral nail corner of the 4th toe at GB44 Zuqiaoyin. An internal collateral branches from GB41 and travels to the great toe nail to link with LR1 Dadun."
            }
        ]
    },
    "LR": {
        "start": {
            "code": "LR1",
            "py": "Dadun",
            "hz": "大敦",
            "en": "Large Pile",
            "landmark": "Lateral Nail Angle · Great Toe",
            "loc": "On the lateral side of the great toe, 0.1 cun posterior to the corner of the nail."
        },
        "end": {
            "code": "LR14",
            "py": "Qimen",
            "hz": "期門",
            "en": "Cycle Gate",
            "landmark": "6th Intercostal Space · Mamillary Line",
            "loc": "In the 6th intercostal space, on the mamillary line, 4 cun lateral to the anterior midline.",
            "handoff": "Internal branch crosses diaphragm into Lungs (LU1) to restart 12-channel cycle"
        },
        "course": "Foot → Chest (Centripetal Yin)",
        "tide": "01:00 – 03:00 · Chou Hour (丑時)",
        "organs": {
            "primary": "Liver (肝 · Zang)",
            "paired": "Gallbladder (膽 · Fu)",
            "tissues": "Tendons · Ligaments · Eyes · Nails · External Genitalia · Hypochondrium"
        },
        "stages": [
            {
                "num": "01",
                "title": "Great Toe Dorsum & Pre-Malleolar Ascent",
                "desc": "Begins at the lateral/dorsal nail angle of the great toe at LR1 Dadun, ascends the dorsum of the foot between the 1st and 2nd metatarsals through LR2 and LR3 Taichong (Yuan-Source), and passes 1 cun anterior to the medial malleolus at LR4 Zhongfeng."
            },
            {
                "num": "02",
                "title": "Tibial Decussation, Medial Knee & Groin",
                "desc": "Ascends the medial margin of the lower leg along the tibia, crosses behind the Spleen channel 8 cun above the ankle, passes the medial end of the popliteal crease at LR8 Ququan, and courses up the medial thigh adductor canal to the pubic crest."
            },
            {
                "num": "03",
                "title": "Genital Encircling & Hypochondriac Terminus",
                "desc": "Curves in a complete ring around the external genitalia, enters the lower abdomen, climbs parallel to the stomach, penetrates the Liver and Gallbladder, and arches through the diaphragm to spread over the costal margin, terminating superficially at LR14 Qimen in the 6th intercostal space."
            },
            {
                "num": "04",
                "title": "Cephalic Vertex Ascent & Pulmonary Handoff",
                "desc": "A deep internal branch ascends through the throat and retro-ocular tissues to reach the vertex of the head at GV20 Baihui. Another internal vessel separates from the Liver, penetrates the diaphragm, and enters the Lungs to connect with LU1 Zhongfu, closing the continuous 12-meridian macro-circulation."
            }
        ]
    }
}

# Update points.json with enriched details
for c in doc['channels']:
    abbr = c['abbr']
    if abbr in CHANNEL_DETAILS:
        info = CHANNEL_DETAILS[abbr]
        c['startDetails'] = info['start']
        c['endDetails'] = info['end']
        c['course'] = info['course']
        c['tide'] = info['tide']
        c['organAffinities'] = info['organs']
        c['stages'] = info['stages']

POINTS_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print("Successfully enriched data/points.json with multi-stage milestone pathways!")
