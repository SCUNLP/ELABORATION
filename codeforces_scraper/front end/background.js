const BASE_URL = "http://118.24.5.98:5000"

// 获取URL、打开页面、执行脚本并关闭页面的函数
async function performTask() {
    try {
        const response = await fetch(`${BASE_URL}/get_url`); // 根据实际情况修改服务器地址和端口
        const data = await response.json();
        const { contestId, id } = data;

        if (contestId && id) {
            const url = `https://codeforces.com/contest/${contestId}/submission/${id}`;
            chrome.tabs.create({ url: url }, function (newTab) {
                chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo, tab) {
                    if (tabId === newTab.id && changeInfo.status === 'complete') {
                        console.log(`Tab ${tabId} completed loading`);

                        chrome.scripting.executeScript(
                            {
                                target: { tabId: tabId },
                                func: () => {
                                    const element = document.getElementById('program-source-text');
                                    if (element) {
                                        return element.textContent;
                                    }
                                    return null;
                                }
                            },
                            (results) => {
                                if (results && results[0].result) {
                                    const solution = results[0].result

                                    if (solution !== "N/A") {
                                        const postData = {
                                            contestId: contestId,
                                            id: id,
                                            solution: solution
                                        };

                                        fetch(`${BASE_URL}/submit`, {
                                            method: 'POST',
                                            headers: {
                                                'Content-Type': 'application/json'
                                            },
                                            body: JSON.stringify(postData)
                                        });
                                    }
                                } else {
                                    console.log('Element not found');
                                }

                                // 关闭标签页
                                chrome.tabs.remove(tabId);
                            }
                        );

                        // 移除监听器
                        chrome.tabs.onUpdated.removeListener(listener);
                    }
                });
            });
        } else {
            console.warn('返回的数据不包含有效的 contestId 和 id:', data);
        }
    } catch (error) {
        // 处理请求错误
        console.error('请求失败:', error);
    }
}

chrome.runtime.onInstalled.addListener(() => {
    // 创建一个每分钟触发的定时器
    chrome.alarms.create('minuteAlarm', { periodInMinutes: 2 });
});

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'minuteAlarm') {
        performTask();
    }
});
