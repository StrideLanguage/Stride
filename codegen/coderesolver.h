#ifndef CODERESOLVER_H
#define CODERESOLVER_H


#include <QVector>
#include <QSharedPointer>

#include "strideplatform.hpp"
#include "stridelibrary.hpp"

#include "ast.h"
#include "streamnode.h"
#include "bundlenode.h"
#include "expressionnode.h"
#include "propertynode.h"
#include "blocknode.h"
#include "namenode.h"
#include "rangenode.h"
#include "valuenode.h"

class CodeResolver
{
public:
    CodeResolver(StridePlatform *platform, AST *tree);
    ~CodeResolver();

    void preProcess();

private:
    // Main processing functions
    void insertBuiltinObjects();
    void fillDefaultProperties();
    void declareModuleInternalBlocks();
    void resolveStreamSymbols();
    void expandParallel();
    void resolveConstants();
    void resolveRates();
    void processDomains();

    // Sub functions
    void resolveStreamRates(StreamNode *stream);
    void expandParallelStream(StreamNode *stream, QVector<AST *> scopeStack, AST *tree);

    void expandStreamToSizes(StreamNode *stream, QVector<int> &size);
    AST *expandFunctionFromProperties(FunctionNode *func, QVector<AST *> scope, AST *tree);
    void fillDefaultPropertiesForNode(AST *node);

    void insertBuiltinObjectsForNode(AST *node, QList<AST *> &objects);

    void processDomainsForStream(StreamNode *func, QVector<AST *> scopeStack);
    string processDomainsForNode(AST *node, QVector<AST *> scopeStack, QList<AST *> &domainStack);
    void setDomainForStack(QList<AST *> domainStack, string domainName,  QVector<AST *> scopeStack);
    BlockNode *createSignalDeclaration(QString name, int size = 1);
    void declareUnknownName(NameNode *name, int size, AST *tree);
    BlockNode *createConstantDeclaration(string name, AST *value);
    void declareIfMissing(string name, AST *blockList, AST *value);

    void declareUnknownExpressionSymbols(ExpressionNode *expr, int size, AST * tree);
    ListNode *expandNameToList(NameNode *name, int size);
    void expandNamesToBundles(StreamNode *stream, AST *tree);
    void declareUnknownStreamSymbols(StreamNode *stream, AST *previousStreamMember, AST *tree);

//    QVector<AST *>  expandStream(StreamNode *stream);
//    void expandStreamMembers();
//    void sliceStreams();

//    void reduceExpressions();
    ValueNode *reduceConstExpression(ExpressionNode *expr, QVector<AST *> scope, AST *tree);
    ValueNode *resolveConstant(AST *value, QVector<AST *> scope);
    void resolveConstantsInNode(AST *node, QVector<AST *> scope);
    void resolveDomainForStreamNode(AST *node, QVector<AST *> scope);

    // Operators
    ValueNode *multiply(ValueNode *left, ValueNode *right);
    ValueNode *divide(ValueNode *left, ValueNode *right);
    ValueNode *add(ValueNode *left, ValueNode *right);
    ValueNode *subtract(ValueNode *left, ValueNode *right);
    ValueNode *unaryMinus(ValueNode *value);
    ValueNode *logicalAnd(ValueNode *left, ValueNode *right);
    ValueNode *logicalOr(ValueNode *left, ValueNode *right);
    ValueNode *logicalNot(ValueNode *left);
    ValueNode *equal(ValueNode *left, ValueNode *right);
    ValueNode *notEqual(ValueNode *left, ValueNode *right);
    ValueNode *greaterThan(ValueNode *left, ValueNode *right);
    ValueNode *lesser(ValueNode *left, ValueNode *right);
    ValueNode *greaterEqual(ValueNode *left, ValueNode *right);
    ValueNode *lesserEqual(ValueNode *left, ValueNode *right);

//    QVector<AST *> expandStreamNode(StreamNode *stream);
//    AST *expandStream(AST *node, int index, int rightNumInputs, int leftNumOutputs);
//    QVector<AST *> sliceStream(StreamNode *stream);
    StreamNode *splitStream(StreamNode *stream, AST *closingNode, AST *endNode);

    // TODO move these four functions to CodeValidator with the rest of querying functions
    double findRateInProperties(vector<PropertyNode *> properties, QVector<AST *> scope, AST *tree);
    double getNodeRate(AST *node, QVector<AST *> scope, AST *tree);
    double getDefaultForTypeAsDouble(QString type, QString port);
    AST *getDefaultPortValueForType(QString type, QString portName);


    StridePlatform *m_platform;
    AST *m_tree;
    int m_connectorCounter;
};

#endif // CODERESOLVER_H
