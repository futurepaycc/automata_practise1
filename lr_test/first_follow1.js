// https://github.com/MikeDevice/first-follow

// 参考: https://bbs.pediy.com/thread-248501.htm

const EMPTY_CHAIN = null;
const END_MARKER = '$';

function firstFollow(rules) {
    let firstSets = {};
    let followSets = {};
    let predictSets = {};

    rules.map(({ left }) => {
        firstSets[left] = [];
        followSets[left] = [];
    });

    function union(arr1, arr2) {
        return [...new Set([...arr1, ...arr2])];
    }

    function isNonterminal(item) {
        return firstSets[item];
    }

    function collectSet(initialSet, items, additionalSet) {
        let set = initialSet;
        // NOTE every和forEach语义差异很大: every是做每项检查，默认返回为false，即不明确返回true即中止
        items.every((item, index) => {
            if (isNonterminal(item)) {
                set = union(set, firstSets[item].filter((setItem) => setItem !== EMPTY_CHAIN));

                if (firstSets[item].includes(EMPTY_CHAIN)) {
                    if (items[index + 1]) return true;
                    set = union(set, additionalSet);
                }
            } else {
                set = union(set, [item]);
                return false
            }
        });

        return set;
    }

    function makeFirstSets() {
        let isSetChanged;

        do {
            isSetChanged = false;

            rules.forEach(({ left, right }) => {
                let set = firstSets[left];
                let collect_set = collectSet(set, right, [EMPTY_CHAIN])
                set = union(set,  collect_set);

                if (firstSets[left].length !== set.length) {
                    firstSets[left] = set;
                    isSetChanged = true;
                }
            });
        } while (isSetChanged);

        return firstSets;
    }

    // 唯一搞定那个怪语法且有源码的! -- 这个看着像虎书算法，不是龙书那个混淆定义！
    function makeFollowSets() {
        followSets[rules[0].left].push(END_MARKER);

        let isSetChanged;

        do {
            isSetChanged = false;

            rules.forEach(({ left, right }) => {
                right.forEach((item, index) => {
                    if (!isNonterminal(item)) return;

                    let set = followSets[item];

                    // NOTE 就这么一句就算好了
                    set = union(
                        set,
                        index + 1 < right.length
                            ? collectSet(set, right.slice(index + 1), followSets[left])
                            : followSets[left],
                    );

                    if (followSets[item].length !== set.length) {
                        followSets[item] = set;
                        isSetChanged = true;
                    }
                });
            });
        } while (isSetChanged);

        return followSets;
    }

    function makePredictSets() {
        rules.forEach(({ left, right }, ruleIndex) => {
            const firstItem = right[0];
            let set = [];

            if (isNonterminal(firstItem)) {
                set = union(set, collectSet(set, right, followSets[left]));
            } else if (firstItem === EMPTY_CHAIN) {
                set = [...followSets[left]];
            } else {
                set.push(firstItem);
            }

            predictSets[ruleIndex + 1] = set;
        });

        return predictSets;
    }

    firstSets = makeFirstSets();
    followSets = makeFollowSets();
    predictSets = makePredictSets();

    return { firstSets, followSets, predictSets };
};


let rules = [
    {
        left: 'S',
        right: ['A', 'C', 'B']
    },
    {
        left: 'S',
        right: ['C', 'b', 'b']
    },
    {
        left: 'S',
        right: ['B', 'a']
    },
    {
        left: 'A',
        right: ['d', 'a']
    },
    {
        left: 'A',
        right: ['B', 'C']
    },
    {
        left: 'B',
        right: ['g']
    },
    {
        left: 'B',
        right: [null]
    },
    {
        left: 'C',
        right: ['h']
    },
    {
        left: 'C',
        right: [null]
    },
];

// 问题, 如果用字面'ϵ'而不用null, follow集计算结果不正确
rules = [
    {left:"E", right:["T","E'"]},
    {left:"E'",right:["+","T","E'"]},
    {left:"E'",right:[null]},
    {left:"T", right:["F","T'"]},
    {left:"T'",right:["*","F","T'"]},
    {left:"T'",right:[null]},
    {left:"F", right:["id"]},
    {left:"F", right:["(","E",")"]},       
];

const { firstSets, followSets, predictSets } = firstFollow(rules);

// console.log(rules)
console.log(firstSets)
console.log(followSets)
console.log(predictSets)