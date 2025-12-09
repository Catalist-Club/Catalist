/**
 * 图片压缩工具
 * 将大于512KB的图片压缩到512KB以下
 */

/**
 * 压缩图片到指定大小（512KB）
 * @param {File|Blob} imageFile - 原始图片文件
 * @param {number} maxSizeKB - 最大文件大小（KB），默认512KB
 * @param {Function} onProgress - 进度回调函数（可选）
 * @returns {Promise<Blob>} 压缩后的图片Blob
 */
async function compressImage(imageFile, maxSizeKB = 512, onProgress = null) {
    // 如果文件已经小于目标大小，直接返回
    const maxSizeBytes = maxSizeKB * 1024;
    if (imageFile.size <= maxSizeBytes) {
        if (onProgress) onProgress(100, '图片无需压缩');
        return imageFile;
    }

    if (onProgress) onProgress(0, '开始压缩图片...');

    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const img = new Image();
            
            img.onload = function() {
                if (onProgress) onProgress(30, '图片加载完成，开始压缩...');
                
                // 计算初始压缩参数
                let quality = 0.9;
                let width = img.width;
                let height = img.height;
                
                // 如果图片很大，先缩小尺寸
                const maxDimension = 2048; // 最大尺寸
                if (width > maxDimension || height > maxDimension) {
                    const ratio = Math.min(maxDimension / width, maxDimension / height);
                    width = Math.floor(width * ratio);
                    height = Math.floor(height * ratio);
                    if (onProgress) onProgress(50, '调整图片尺寸...');
                }
                
                // 创建canvas进行压缩
                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                
                // 绘制图片
                ctx.drawImage(img, 0, 0, width, height);
                
                // 尝试不同的质量值，直到文件大小符合要求
                const tryCompress = (currentQuality) => {
                    if (onProgress) {
                        const progress = 50 + (0.9 - currentQuality) * 50;
                        onProgress(Math.floor(progress), `压缩中... (质量: ${Math.round(currentQuality * 100)}%)`);
                    }
                    
                    canvas.toBlob((blob) => {
                        if (!blob) {
                            reject(new Error('图片压缩失败'));
                            return;
                        }
                        
                        // 如果文件大小符合要求，或者质量已经很低了，返回结果
                        if (blob.size <= maxSizeBytes || currentQuality <= 0.1) {
                            if (onProgress) {
                                const savedPercent = Math.round((1 - blob.size / imageFile.size) * 100);
                                onProgress(100, `压缩完成！原始大小: ${(imageFile.size / 1024).toFixed(1)}KB, 压缩后: ${(blob.size / 1024).toFixed(1)}KB (节省 ${savedPercent}%)`);
                            }
                            resolve(blob);
                        } else {
                            // 继续降低质量
                            const nextQuality = Math.max(0.1, currentQuality - 0.1);
                            tryCompress(nextQuality);
                        }
                    }, 'image/jpeg', currentQuality);
                };
                
                // 开始压缩
                tryCompress(quality);
            };
            
            img.onerror = function() {
                reject(new Error('图片加载失败'));
            };
            
            img.src = e.target.result;
        };
        
        reader.onerror = function() {
            reject(new Error('文件读取失败'));
        };
        
        reader.readAsDataURL(imageFile);
    });
}

/**
 * 批量压缩图片
 * @param {File[]} imageFiles - 图片文件数组
 * @param {number} maxSizeKB - 最大文件大小（KB），默认512KB
 * @param {Function} onProgress - 进度回调函数 (index, total, message)
 * @returns {Promise<Blob[]>} 压缩后的图片Blob数组
 */
async function compressImages(imageFiles, maxSizeKB = 512, onProgress = null) {
    const results = [];
    const total = imageFiles.length;
    
    for (let i = 0; i < imageFiles.length; i++) {
        if (onProgress) {
            onProgress(i + 1, total, `正在压缩第 ${i + 1}/${total} 张图片...`);
        }
        
        const compressed = await compressImage(imageFiles[i], maxSizeKB);
        results.push(compressed);
    }
    
    if (onProgress) {
        onProgress(total, total, '所有图片压缩完成！');
    }
    
    return results;
}

// 导出函数（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { compressImage, compressImages };
}
