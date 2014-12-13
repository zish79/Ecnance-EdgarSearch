from django.http import HttpResponse
import django.db
import urllib2, urllib
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
from symbol import if_stmt
#from test.test_bisect import Range
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.template import loader
from ecnance.models import CIKPage, companies, ticker_data, ticker_data_new
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
# import xml.etree.ElementTree as ET
from xml.etree import ElementTree as ET
# from elementtree.ElementTree import * as Element
# from xml.etree import ElementTree as ET
import json
import time
from array import *
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

Left_Dict = {}
Chart_Dict_IS={}
Chart_Dict_CS={}
Chart_Dict_BS={}
Chart_Dict_SE={}

def getInnerString(myString):
    mySubString=myString[myString.find("{"):myString.find("}")+1]
    return mySubString

def Gross_profit_margin():
    try:
        if not Left_Dict.has_key("CostOfRevenue"):
            Left_Dict["CostOfRevenue"] = 0 
        if not Left_Dict.has_key("Revenues"):
            Left_Dict["Revenues"] = 0 
        temp = float(Left_Dict["Revenues"]) - float(Left_Dict["CostOfRevenue"])
        if Left_Dict["Revenues"] and Left_Dict["Revenues"]!=0:
            return float(temp) / float(Left_Dict["Revenues"])
        else:
            return 0.0
    except:
        return 0.0

def Operating_Profit_Margin():
    try:
        if not Left_Dict.has_key("OperatingIncomeLoss"):
            Left_Dict["OperatingIncomeLoss"] = 0
        if Left_Dict["Revenues"] and Left_Dict["Revenues"]!=0:
            return float(Left_Dict["OperatingIncomeLoss"]) / float(Left_Dict["Revenues"])
        else:
            return 0.0
    except:
        return 0.0
def Quick_Ratio():
    try:
        if not Left_Dict.has_key("AssetsCurrent"):
            Left_Dict["AssetsCurrent"] = 0
        if not Left_Dict.has_key("InventoryNet"):
            Left_Dict["InventoryNet"] = 0
        temp = float(Left_Dict["AssetsCurrent"]) - float(Left_Dict["InventoryNet"])
        
        if Left_Dict["LiabilitiesCurrent"] and Left_Dict["LiabilitiesCurrent"]!=0:
            return float(temp) / float(Left_Dict["LiabilitiesCurrent"])
        else:
            return 0.0
    except:
        return 0.0
def Equity_Ratio():
    try:
        if not Left_Dict.has_key("LongTermDebtNoncurrent"):
           Left_Dict["LongTermDebtNoncurrent"] = 0 
        if not Left_Dict.has_key("ShortTermBorrowings"):
           Left_Dict["ShortTermBorrowings"] = 0
        if Left_Dict["Assets"] and float(Left_Dict["Assets"]!=0):
            temp = float(Left_Dict["LongTermDebtNoncurrent"]) / float(Left_Dict["Assets"])
        else:
            temp = 0.0
        return float(temp) + float(Left_Dict["ShortTermBorrowings"])
    except:
        return 0.0
    
def Return_on_Equity():
    try:
        if not Left_Dict.has_key("NetIncomeLoss"):
           Left_Dict["NetIncomeLoss"] = 0 
        if not Left_Dict["StockholdersEquity"] and  Left_Dict["StockholdersEquity"]!=0:
            return float(Left_Dict["NetIncomeLoss"]) / float(Left_Dict["StockholdersEquity"])
        else:
           return 0.0 
    except:
        return 0.0
           
    
def Assets_Turnover():
    try:
        if not Left_Dict.has_key("Revenues"):
           Left_Dict["Revenues"] = 0
        if Left_Dict["Assets"] and  Left_Dict["Assets"]!=0:
            return float(Left_Dict["Revenues"]) / float(Left_Dict["Assets"])
        else:
            return 0.0
    except:
        return 0.0

def Debt_To_Equity():
    try:
        if not Left_Dict.has_key("LiabilitiesCurrent"):
            Left_Dict["LiabilitiesCurrent"] = 0 
        if not Left_Dict.has_key("LongTermDebtNoncurrent"):
            Left_Dict["LongTermDebtNoncurrent"] = 0
        if not Left_Dict.has_key("DeferredRevenueNoncurrent"):
            Left_Dict["DeferredRevenueNoncurrent"] = 0 
        if not Left_Dict.has_key("DeferredTaxLiabilitiesNoncurrent"):
            Left_Dict["DeferredTaxLiabilitiesNoncurrent"] = 0
        if not Left_Dict.has_key("OtherLiabilitiesNoncurrent"):
            Left_Dict["OtherLiabilitiesNoncurrent"] = 0
        temp = (float(Left_Dict["LiabilitiesCurrent"]) + (float(Left_Dict["LongTermDebtNoncurrent"]) + float(Left_Dict["DeferredRevenueNoncurrent"]) + float(Left_Dict["DeferredTaxLiabilitiesNoncurrent"]) + float(Left_Dict["OtherLiabilitiesNoncurrent"])))
        if Left_Dict["StockholdersEquity"] and  Left_Dict["StockholdersEquity"]!=0:
            return float(temp) / float(Left_Dict["StockholdersEquity"])
        else:
            return 0.0
    except:
        return 0.0
    
def Inventory_Turnover():
    try:
        if not Left_Dict.has_key("Revenues"):
            Left_Dict["Revenues"] = 0 
        if Left_Dict["InventoryNet"] and  Left_Dict["InventoryNet"]!=0:
            return float(Left_Dict["Revenues"]) / float(Left_Dict["InventoryNet"])
        else:
            return 0.0
    except:
        return 0.0
    
def Long_Term_Debt_to_Capitalization_Ratio():
    try:
        if not Left_Dict.has_key("PreferredStockSharesOutstanding"):
            Left_Dict["PreferredStockSharesOutstanding"] = 0 
        if Left_Dict.has_key("PreferredStockSharesOutstanding") is None:
            Left_Dict["PreferredStockSharesOutstanding"] = 0 
        if not Left_Dict.has_key("LongTermDebtNoncurrent"):
            Left_Dict["LongTermDebtNoncurrent"] = 0
        if Left_Dict.has_key("CommonStockSharesOutstanding") is None:
            Left_Dict["CommonStockSharesOutstanding"] = 0
        if not Left_Dict.has_key("CommonStockSharesOutstanding"):
            Left_Dict["CommonStockSharesOutstanding"] = 0 
        if Left_Dict.has_key("CommonStockSharesOutstanding") is None:
            Left_Dict["CommonStockSharesOutstanding"] = 0
        temp = float(Left_Dict["LongTermDebtNoncurrent"]) + float(Left_Dict["PreferredStockSharesOutstanding"]) + float(Left_Dict["CommonStockSharesOutstanding"])
        if temp != 0:
            return float(Left_Dict["LongTermDebtNoncurrent"]) / float(temp)
        else:
            return 0.0
    except:
        return 0.0
    
def Check_Max(max, dollar):
    doll = dollar
    ma = max
    try:
        maa = int(ma)
        dolla = int(doll)
    except:
        print("Exception")
    try:
        if('-' in dollar):
            return max
        if float(max) >= float(dollar) :
            return max
        else:
            return dollar
    except:
        print("Exception1")
 
def BalanceSheet_Table(root, year, list,list_PreURL_Data):
    flag1 = True
    flag2 = True
    byea = str(year - 1)
    yea = str(year)
    tabl = "<table class='table'><tr><th>Balance Sheet Statements</th><th>" + yea + " Year Data</th><th>" + byea + "Year Data</th></tr>"
    tabl += "<tr><th>Assets</th></tr>"
    Label = ""
    for tags in list:
        for each_URL in list_PreURL_Data:
            max1 = 0
            max2 = 0
            data = root.findall("./{"+each_URL+'}'+ tags)
            if data:
                for child in data:
                    msg_attrs = child.get('contextRef')
                    if not child.text is None:
                        if yea in msg_attrs:
                            max1 = Check_Max(max1, child.text)
                        if byea in msg_attrs:
                            max2 = Check_Max(max2, child.text)
                if tags == 'AssetsCurrentAbstract':
                    Label = 'Current assets'
                if tags == 'CashAndCashEquivalentsAtCarryingValue':
                    Label = 'Cash and cash equivalents'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["CashAndCashEquivalentsAtCarryingValue"] = (temp_C/float(max2))*100
                if tags == 'AvailableFroSaleSecuritiescurrent':
                    Label = 'Marketable securities'
                if tags == 'CashCashEquivalentsAndShortTermInvestments':
                    Label = 'Total cash, cash equivalents, and marketable securities (including securities loaned of $3,160 and $4,155)'
                if tags == 'AccountsReceivableNetCurrent':
                    Label = 'Accounts receivable, net of allowance of $581 and $533)'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["AccountsReceivableNetCurrent"] = (temp_C/float(max2))*100
                if tags == 'InventoryNet':
                    Label = 'Receivable under reverse repurchase agreements'
                    Left_Dict["InventoryNet"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["InventoryNet"] = (temp_C/float(max2))*100
                if tags == 'DeferredTaxAssetsNetcurrent':
                    Label = 'Deferred income taxes, net'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["DeferredTaxAssetsNetcurrent"] = (temp_C/float(max2))*100
                if tags == 'IncomeTaxesReceivable':
                    Label = 'Income taxes receivable, net'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["IncomeTaxesReceivable"] = (temp_C/float(max2))*100
                if tags == 'PrepaidRevenueShareExpensesAndOtherAssetsCurrent':
                    Label = 'Prepaid revenue share, expenses and other assets'
                if tags == 'AssetsCurrent':
                    Label = 'Total current assets'
                    Left_Dict["AssetsCurrent"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["AssetsCurrent"] = (temp_C/float(max2))*100
                if tags == 'PreferredStockSharesOutstanding':
                    Label = 'Preferred Stock Shares Outstanding'
                    Left_Dict["PreferredStockSharesOutstanding"] = max1
                if tags == 'CommonStockSharesOutstanding':
                    Label = 'Common Stock Shares Outstanding'
                    Left_Dict["CommonStockSharesOutstanding"] = max1
                if tags == 'PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent':
                    Label = 'Prepaid revenue share, expenses and other assets, non-current'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent"] = (temp_C/float(max2))*100
                if tags == 'OtherLongTermInvestments':
                    Label = 'Non-marketable equity investments'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["OtherLongTermInvestments"] = (temp_C/float(max2))*100
                if tags == 'PropertyPlantAndEquipmentNet':
                    Label = 'Property and equipment, net'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["PropertyPlantAndEquipmentNet"] = (temp_C/float(max2))*100
                if tags == 'IntangibleAssetsNetExcludingGooldwill':
                    Label = 'Intangible assets, net'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["IntangibleAssetsNetExcludingGooldwill"] = (temp_C/float(max2))*100
                if tags == 'Goodwill':
                    Label = 'Goodwill'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["Goodwill"] = (temp_C/float(max2))*100
                if tags == 'Assets':
                    Label = 'Total assets'
                    Left_Dict["Assets"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_BS["Assets"] = (temp_C/float(max2))*100
                if tags == 'AccountsPayableCurrent':
                    Label = 'Account payable'
                if tags == 'ShortTermBorrowings':
                    Label = 'Short-term debt'
                    Left_Dict["ShortTermBorrowings"] = max1
                if tags == 'EmployeeRelatedLiabilitesCurrent':
                    Label = 'Accrued compensations and benefits'
                if tags == 'AccruedLiabilitesCurrent':
                    Label = 'Accrued expenses and other current liabilities'
                if tags == 'DepositsReceivedForSecuritiesLoanedAtCarryingValue':
                    Label = 'Accrued revenue share'
                if tags == 'DeferredRevenueCurrent':
                    Label = 'Deferred revenue'
                if tags == 'AccruedIncomeTaxesCurrent':
                    Label = 'Income taxes payable, net'
                if tags == 'LiabilitiesCurrent':
                    Label = 'Total current liabilities'
                    Left_Dict["LiabilitiesCurrent"] = max1
                if tags == 'LongTermDebtNoncurrent':
                    Label = 'Long-term debt'
                    Left_Dict["LongTermDebtNoncurrent"] = max1
                if tags == 'DeferredRevenueNoncurrent':
                    Label = 'Deferred revenue, non-current'
                    Left_Dict["DeferredRevenueNoncurrent"] = max1
                if tags == 'LiabilityForUncertainTaxPositionsNoncurrent':
                    Label = 'Income taxes payable, non-current'
                if tags == 'DeferredTaxLiabilitiesNoncurrent':
                    Label = 'Deferred income taxes, net, non-current'
                    Left_Dict["DeferredTaxLiabilitiesNoncurrent"] = max1
                if tags == 'OtherLiabilitiesNoncurrent':
                    Label = 'Other long-term liabilities'
                    Left_Dict["OtherLiabilitiesNoncurrent"] = max1
                if tags == 'ConvertablePreferredStockNonRedeemableOrRedeemableIssuerOptionValue':
                    Label = 'Convertible preferred stock, $0.001 par value per share, 100,000 shares authorized; no shares issued and outstanding'
                if tags == 'AccumulatedOtherComprehensiveIncomeLossNetOfTax':
                    Label = 'Accumulated other comprehensive income'
                if tags == 'RetainedEarningsAccumulatedDeficit':
                    Label = 'Retained earning'
                if tags == 'LiabilitiesAndStockholdersEquity':
                    Label = 'Total liabilities and stockholders equity'
                if tags == 'AccountsPayableCurrent' or tags == 'ShortTermBorrowings' or tags == 'EmployeeRelatedLiabilitesCurrent' or tags == 'AccruedLiabilitesCurrent' or tags == 'DepositsReceivedForSecuritiesLoanedAtCarryingValue' or tags == 'DeferredRevenueCurrent' or tags == 'AccruedIncomeTaxesCurrent' or tags == 'LiabilitiesCurrent' or tags == 'LongTermDebtNoncurrent' or tags == 'DeferredRevenueNoncurrent' or tags == 'LiabilityForUncertainTaxPositionsNoncurrent' or tags == 'DeferredTaxLiabilitiesNoncurrent' or tags == 'OtherLiabilitiesNoncurrent':
                    if flag1:
                        tabl += "<tr><th>Liabilities and Stockholders Equity</th></tr>"
                        tabl += "<tr><th>        Current liabilities</th></tr>"
                        flag1 = False
                if tags == 'ConvertablePreferredStockNonRedeemableOrRedeemableIssuerOptionValue' or tags == 'AccumulatedOtherComprehensiveIncomeLossNetOfTax' or tags == 'RetainedEarningsAccumulatedDeficit' or tags == 'LiabilitiesAndStockholdersEquity':
                    if flag2:
                        tabl += "<tr><th>Stockholders equity</th></tr>"
                        flag2 = False
                tabl += "<tr><td>" + str(Label) + "</td><td>$" + str(max1) + "</td><td>$" + str(max2) + "</td></tr>"
    tabl += "</table>"
    return tabl    
    
def CashFlowStatement_Table(root, year, list,list_PreURL_Data):
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True
    flag5 = True
    flag6 = True
    Label = ""
    byea =str(year - 1)
    yea = str(year)
    tabl = "<table class='table1'><tr><th>Cashflow Statements</th><th>" + yea + " Year Data</th><th>" + byea + "Year Data</th></tr>"
    tabl += "<tr><th>Operating activities</th></tr>"
    for tags in list:
        for each_URL in list_PreURL_Data:
            max1 = 0
            max2 = 0
            data = root.findall("./{"+each_URL+'}'+ tags)
            if data:
                for child in data:
                    msg_attrs = child.get('contextRef')
                    if not child.text is None:
                        if yea in msg_attrs:
                            max1 = Check_Max(max1, child.text)
                        if byea in msg_attrs:
                            max2 = Check_Max(max2, child.text)
                if tags == 'NetIncomeLoss':
                    Label = 'Net income'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["NetIncomeLoss"] = (temp_C/float(max2))*100   
                if tags == 'Depreciation':
                    Label = 'Depreciation and amortization of property and equipment'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["Depreciation"] = (temp_C/float(max2))*100 
                if tags == 'AmortizationOfIntangibleAssets':
                    Label = 'Amortization of intangible and other assets'
                if tags == 'ShareBasedCompensation':
                    Label = 'Stock-based compensation expense'
                if tags == 'DeferredIncomeTaxExpenseBenifit':
                    Label = 'Deferred income taxes'
                if tags == 'MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments':
                    Label = 'Gain on sale of marketable equity securities'
                if tags == 'OtherNonCashIncomeExpense':
                    Label = 'Other '
                if tags == 'IncreaseDecreaseInAccountsReceivable':
                    Label = 'Accounts receivable'
                if tags == 'IncreaseDecreaseInInventories':
                    Label = 'Inventories '
                if tags == 'IncreaseDecreaseInOtherCurrentAssets':
                    Label = 'Other current assets'
                if tags == 'IncreaseDecreaseInOtherNoncurrentAssets':
                    Label = 'Other long-term assets'
                if tags == 'IncreaseDecreaseInAccountsPayable':
                    Label = 'Accounts payable'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["IncreaseDecreaseInAccountsPayable"] = (temp_C/float(max2))*100 
                if tags == 'IncreaseDecreaseInDeferredRevenue':
                    Label = 'Deferred revenue'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["IncreaseDecreaseInDeferredRevenue"] = (temp_C/float(max2))*100 
                if tags == 'IncreaseDecreaseInOtherCurrentLiabilities':
                    Label = 'Other current liabilities'
                if tags == 'IncreaseDecreaseInOtherNoncurrentAssets':
                    Label = 'Other long-term liabilities'
                if tags == 'NetCashProvidedByUsedInOperatingActivities':
                    Label = 'Net cash provided by operating activities'
                if tags == 'PaymentToAcquireMarketingSecurities':
                    Label = 'Purchases of marketable securities'
                if tags == 'ProceedsFromSaleAndMaturityOfMarketableSecurities':
                    Label = 'Maturities and sales of marketable securities'
                if tags == 'PaymentsToAcquireOtherInvestments':
                    Label = 'Investment in non-marketable equity investments'
                if tags == 'IncreaseDecreaseInCollateralHeldUnderSecuritiesLending':
                    Label = 'Cash collateral related to securities lending'
                if tags == 'InvestmentsInReverseRepurchaseAgreements':
                    Label = 'Investments in reverse re purchase agreements'
                if tags == 'AcquisitionsNetOfCashAcquiredAndPurchasesOfIntangiblesandOtherAssets':
                    Label = 'Acquisitions, net of cash acquired, and purchases of intangibles and other assets'
                if tags == 'NetCashProvidedByUseInInvestingActivities':
                    Label = 'AcquisitionsNetOfCashAcquiredAndPurchasesOfIntangiblesandOtherAssets Net cash provided by (use in) investing activities'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["NetCashProvidedByUseInInvestingActivities"] = (temp_C/float(max2))*100
                if tags == 'ExcessTaxBenifitFromShareBasedCompensationFinancingActivities':
                    Label = 'Excess tax benefits from stock-based award activities'
                if tags == 'ProceedsFromDebtNetOfIssanceCosts':
                    Label = 'Proceeds from issuance of debts, net of costs'
                if tags == 'RepaymentsOfDebt':
                    Label = 'Repayments of debts'
                if tags == 'NetCashProvidedByUsedInFinancingActivities':
                    Label = 'Net cash used in financing activities'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["NetCashProvidedByUsedInFinancingActivities"] = (temp_C/float(max2))*100
                if tags == 'EffectOfExchangeRateOnCashAndCashEquivalents':
                    Label = 'Effect of exchange rate changes on cash and cash equivalents'
                if tags == 'CashAndCashEquivalentPeriodIncreaseDecrease':
                    Label = 'Net increase in cash and cash equivalents'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["CashAndCashEquivalentPeriodIncreaseDecrease"] = (temp_C/float(max2))*100
                if tags == 'CashAndCashEquivalentsAtCarryingValue':
                    Label = 'Cash and cash equivalents at beginning of period'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_CS["CashAndCashEquivalentsAtCarryingValue"] = (temp_C/float(max2))*100
                if tags == 'IncomeTaxesPaid':
                    Label = 'Cash paid for taxes'
                if tags == 'Depreciation' or tags == 'AmortizationOfIntangibleAssets' or tags == 'ShareBasedCompensation' or tags == 'DeferredIncomeTaxExpenseBenifit' or tags == 'MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments' or tags == 'OtherNonCashIncomeExpense':
                    if flag1:
                        tabl += "<tr><th>Adjustments</th></tr>"
                        flag1 = False
                if tags == 'IncreaseDecreaseInAccountsReceivable' or tags == 'IncreaseDecreaseInInventories' or tags == 'IncreaseDecreaseInOtherCurrentAssets' or tags == 'IncreaseDecreaseInOtherNoncurrentAssets' or tags == 'IncreaseDecreaseInAccountsPayable' or tags == 'IncreaseDecreaseInDeferredRevenue' or tags == 'IncreaseDecreaseInOtherCurrentLiabilities' or tags == 'IncreaseDecreaseInOtherNoncurrentAssets':
                    if flag3:
                        tabl += "<tr><th>Charges in assets and liabilities, net of effect of acquisitions</th></tr>"
                        flag3 = False
                if tags == 'NetCashProvidedByUsedInOperatingActivities':
                    if flag4:
                        tabl += "<tr><th>Net cash provided by operating activities</th></tr>"
                        flag4 = False
                if tags == 'PaymentToAcquireMarketingSecurities' or tags == 'ProceedsFromSaleAndMaturityOfMarketableSecurities' or tags == 'PaymentsToAcquireOtherInvestments' or tags == 'IncreaseDecreaseInCollateralHeldUnderSecuritiesLending' or tags == 'InvestmentsInReverseRepurchaseAgreements' or tags == 'AcquisitionsNetOfCashAcquiredAndPurchasesOfIntangiblesandOtherAssets' or tags == 'NetCashProvidedByUseInInvestingActivities':
                    if flag5:
                        tabl += "<tr><th>Investing activities</th></tr>"
                        flag5 = False
                if tags == 'ExcessTaxBenifitFromShareBasedCompensationFinancingActivities' or tags == 'ProceedsFromDebtNetOfIssanceCosts' or tags == 'RepaymentsOfDebt' or tags == 'NetCashProvidedByUsedInFinancingActivities' or tags == 'EffectOfExchangeRateOnCashAndCashEquivalents' or tags == 'CashAndCashEquivalentPeriodIncreaseDecrease' or tags == 'CashAndCashEquivalentsAtCarryingValue' or tags == 'CashAndCashEquivalentsAtCarryingValue':
                    if flag6:
                        tabl += "<tr><th>Financing Activities</th></tr>"
                        flag6 = False
                if tags == 'IncomeTaxesPaid':
                    if flag2:
                        tabl += "<tr><th>Supplemental disclosures of cash flow information</th></tr>"
                        flag2 = False
                
                tabl += "<tr><td>" + str(Label) + "</td><td>$" + str(max1) + "</td><td>$" + str(max2) + "</td></tr>"
    tabl += "</table>"
    return tabl 

def IncomeStatement_Table(root, year, list,list_PreURL_Data):
#     print(root.tag)
#     for ccc in root:
#         print(ccc.tag)
#         print(ccc.attrib)
    flag1 = True
    flag2 = True
    byea =  str(year - 1)
    yea =  str(year)
    tabl = "<table class='table2'><tr><th>Income Statements</th><th>" + yea + " Year Data</th><th>" + byea + "Year Data</th></tr>"
    tabl += "<tr><th>Revenues</th></tr>"
    tabl += "<tr><th>Costs and expenses</th></tr>"
    Label = ""
    for tags in list:
        for each_URL in list_PreURL_Data:
            max1 = 0
            max2 = 0
#             sometime_check=getInnerString(str(ccc.tag))
            data = root.findall("./{"+each_URL+'}'+ tags)
            if data:
                for child in data:
                    msg_attrs = child.get('contextRef')
                    if not child.text is None:
                        if yea in msg_attrs:
                            max1 = Check_Max(max1, child.text)
                        if byea in msg_attrs:
                            max2 = Check_Max(max2, child.text)
                if tags == 'Revenues' or tags == 'SalesRevenueNet':
                    Label = 'Revenues'
                    Left_Dict["Revenues"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["Revenues"] = (temp_C/float(max2))*100
                if tags == 'CostOfRevenue':
                    Label = 'Cost of revenues'
                    Left_Dict["CostOfRevenue"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["CostOfRevenue"] = (temp_C/float(max2))*100
                if tags == 'ResearchAndDevelepmentExpense':
                    Label = 'Research and development Expense'
                if tags == 'SellingAndMarketingExpense':
                    Label = 'Sales and marketing Expense'
                if tags == 'GeneralAndAdministrativeExpense':
                    Label = 'General and administrative'
                if tags == 'CostsAndExpenses':
                    Label = 'Total costs and expenses'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["CostsAndExpenses"] = (temp_C/float(max2))*100
                if tags == 'OperatingIncomeLoss':
                    Label = 'Income from operations'
                    Left_Dict["OperatingIncomeLoss"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["OperatingIncomeLoss"] = (temp_C/float(max2))*100
                if tags == 'NonoperatingIncomeExpense':
                    Label = 'Interest and other income, net'
                if tags == 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityAndIncomeLossFromEquityMethodInvestments':
                    Label = 'Income from continuing operations before income taxes'
                if tags == 'IncomeTaxExpenseBenefit':
                    Label = 'Provision from income taxes'
                if tags == 'IncomeLossFromContinuingOperations':
                    Label = 'Net income from continuing operation'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["IncomeLossFromContinuingOperations"] = (temp_C/float(max2))*100
                if tags == 'IncomeLossFromDiscontinuedOperationsNetOfTax':
                    Label = 'Net income from discontinued operations'
                if tags == 'NetIncomeLoss':
                    Label = 'Net income'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_IS["NetIncomeLoss"] = (temp_C/float(max2))*100
                if tags == 'IncomelossFromContinuingOperationsPerBasicshare':
                    Label = 'Continuing operations (in dollars per share)'
                if tags == 'IncomelossfromdiscontinuedOperationsNetOfTaxPerBasicshare':
                    Label = 'Discontinued operations (in dollars per share)'
                if tags == 'EarningsPershareBasic':
                    Label = 'Net income per share-basic (in dollars per share) '
                if tags == 'IncomeLossFromContinuingOperationsPerDilutedShare':
                    Label = 'Continuing operations (in dollars per share)'
                if tags == 'IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedshare':
                    Label = 'Discontinued operations (in dollars per share)'
                if tags == 'EarningsPerShareDiluted':
                    Label = 'Net income per share diluted (in dollars per share)'
                if tags == 'WeightedAverageNumberOfSharesOutstandingBasic':
                    Label = 'Share used in per calculation_ basic'
                if tags == 'WeightedAverageNumberOfDilutedSharesOutstanding':
                    Label = 'Shares used in per share calculation _ diluted'
                if tags == 'IncomelossFromContinuingOperationsPerBasicshare' or tags == 'IncomelossfromdiscontinuedOperationsNetOfTaxPerBasicshare' or tags == 'EarningsPershareBasic':
                    if flag1:
                        tabl += "<tr><th>Net income per share of Class A and Class b common stock-basic </th></tr>"
                        flag1 = False
                if tags == 'IncomeLossFromContinuingOperationsPerDilutedShare' or tags == 'IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedshare' or tags == 'EarningsPerShareDiluted' or tags == 'WeightedAverageNumberOfSharesOutstandingBasic' or tags == 'WeightedAverageNumberOfDilutedSharesOutstanding':
                    if flag2:
                        tabl += "<tr><th>Diluted</th></tr>"
                        flag2 = False
                tabl += "<tr><td>" + str(Label) + "</td><td>$" + str(max1) + "</td><td>$" + str(max2) + "</td></tr>"
    tabl += "</table>"
    return tabl

def ShareholdersEquity_Table(root, year, list,list_PreURL_Data):
    flag1 = True
    flag2 = True
    flag3 = True
    flag4 = True
    flag5 = True
    flag6 = True
    Label = ""
    byea = str(year - 1)
    yea = str(year)
    tabl = "<table class='table3'><tr><th>Shareholders Equity Statements</th><th>" + yea + " Year Data</th><th>" + byea + "Year Data</th></tr>"
    tabl += "<tr><th>Total :</th></tr>"
    for tags in list:
        for each_URL in list_PreURL_Data:
            max1 = 0
            max2 = 0
            data = root.findall("./{"+each_URL+'}'+ tags)
            if data:
                for child in data:
                    msg_attrs = child.get('contextRef')
                    if not child.text is None:
                        if yea in msg_attrs:
                            max1 = Check_Max(max1, child.text)
                        if byea in msg_attrs:
                            max2 = Check_Max(max2, child.text)
                if tags == 'StockholdersEquity':
                    Label = 'Balance- beginning of period'
                    Left_Dict["StockholdersEquity"] = max1
                if tags == 'NetIncomeLoss':
                    Label = 'Net Income'
                    Left_Dict["NetIncomeLoss"] = max1
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_SE["NetIncomeLoss"] = (temp_C/float(max2))*100 
                if tags == 'OhterComprehensiveIncomeLossNetOfTax':
                    Label = 'Other comprehensive income (loss)'
                if tags == 'DividendsCommonStockCash':
                    Label = 'Common stock cashed dividends'
                if tags == 'StockRepurchasedDuringPeriodValue':
                    Label = 'Common stock re purchased'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_SE["StockRepurchasedDuringPeriodValue"] = (temp_C/float(max2))*100 
                if tags == 'StockholdersEquity':
                    Label = 'Balance- end of period'
                if tags == 'CommonStockIncludingAdditionalPaidInCapitalMember':
                    Label = 'Common stock and pain-in capital'
                if tags == 'StockIssuedDuringPeriodValueNewIssues':
                    Label = 'Common stock issued'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_SE["StockIssuedDuringPeriodValueNewIssues"] = (temp_C/float(max2))*100 
                if tags == 'StockRepurchasedDuringPeriodValue':
                    Label = 'Common stock re purchased'
                if tags == 'AdjustmentsToAdditionalPaidInCapitalShareBasedCompensationRequisiteServicePeriodRecognitionValue':
                    Label = 'Stock-based compensation expense'
                if tags == 'AdjustmentToAdditionalPaidInCapitalIncomeTaxEffectFromShareBasedCompensationNet':
                    Label = 'Stock-based compensation income tax benefits (deficiencies)'
                if tags == 'ShareholdersEquityOther':
                    Label = 'Other net'
                    temp_C= float(max1)-float(max2)
                    if float(max2)!=0:
                        Chart_Dict_SE["ShareholdersEquityOther"] = (temp_C/float(max2))*100 
                if tags == 'ShareholdersEquity':
                    Label = 'Balance, end of period'
                if tags == 'RetainedEarningsMember':
                    Label = 'Retained Earnings (deficit)'
                if tags == 'NetIncomeLoss':
                    Label = 'Net income'
                if tags == 'DividendsCommonStockCash':
                    Label = 'Common stock cash dividends'
                if tags == 'StockRepurchasedDuringPeriodValue':
                    Label = 'Common stock re purchased'
                if tags == 'CommonStockIncludingAdditionalPaidInCapitalMember' or tags == 'StockholdersEquity' or tags == 'StockIssuedDuringPeriodValueNewIssues' or tags == 'StockRepurchasedDuringPeriodValue' or tags == 'AdjustmentsToAdditionalPaidInCapitalShareBasedCompensationRequisiteServicePeriodRecognitionValue' or tags == 'AdjustmentToAdditionalPaidInCapitalIncomeTaxEffectFromShareBasedCompensationNet' or tags == 'ShareholdersEquityOther' or tags == 'ShareholdersEquity':
                    Label = 'Other comprehensive income (loss)'
                    
                if tags == 'IncomelossFromContinuingOperationsPerBasicshare' or tags == 'IncomelossfromdiscontinuedOperationsNetOfTaxPerBasicshare' or tags == 'EarningsPershareBasic':
                    if flag1:
                        tabl += "<tr><th>Common stock and pain-in capital</th></tr>"
                        flag1 = False
                if tags == 'RetainedEarningsMember' or tags == 'NetIncomeLoss' or tags == 'DividendsCommonStockCash' or tags == 'StockRepurchasedDuringPeriodValue':
                    if flag2:
                        tabl += "<tr><th>Retained Earnings (deficit)</th></tr>"
                        flag2 = False
                if tags == 'OtherComprehensiveIncomeLossNetOfTax':
                    if flag3:
                        tabl += "<tr><th>Accumulated other comprehensive income</th></tr>"
                        flag3 = False
                tabl += "<tr><td>" + str(Label) + "</td><td>$" + str(max1) + "</td><td>$" + str(max2) + "</td></tr>"
    tabl += "</table>"
    return tabl 

@csrf_protect
def myFirstView(request):
#     matrix=[2][9]
    #matrix = [[0 for x in xrange(9)] for x in xrange(2)] 
    yearp=["",""]
    xbrl_URL=["",""]
    Ycounter=0
    TableBS = ["",""]
    TableIS = ["",""]
    TableCF = ["",""]
    TableSE = ["",""]
    keyRatioStrng = ["",""]
    ChartStrng_BS = ["",""]
    ChartStrng_CS = ["",""]
    ChartStrng_IS = ["",""]
    ChartStrng_SE = ["",""]
    cikVal = ""
    yea = ""
    response = "<html><body>"
    resp = HttpResponse()
    templ = get_template("polls/Statements.html")
    if request.method == 'POST':
        fom = CIKPage(request.POST)
        if fom.is_valid() is None:
            return HttpResponse("The Fields date is invalid!")
        else:
            cikVal = fom.cleaned_data['cik']
#             yea = fom.cleaned_data['year']
            # URL Data Values
            
            CIK_Value = cikVal
#             DATE = str(int(yea)+1)+"0101"
            DATA_COUNT = "100"
        #     ye = "2013"
            url = "http://www.sec.gov"
#             url_id = ""
#             temp = ""
            _CONSOLIDATED_BALANCE_SHEETS = ""
            _CONSOLIDATED_STATEMENTS_OF_SHAREHOLDERS_EQUITY = ""
            _CONSOLIDATED_STATEMENTS_OF_CASHFLOWS = ""
            _CONSOLIDATED_STATEMENTS_OF_INCOME = ""
            # END URL Data Values
            bibi="http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + CIK_Value + "&type=10-K&dateb=&owner=include&count=" + DATA_COUNT
            Main_Page = urllib2.urlopen("http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + CIK_Value + "&type=10-K&dateb=&owner=include&count=" + DATA_COUNT)
#             my="http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + CIK_Value + "&type=10-K&dateb=" + DATE + "&owner=include&count=" + DATA_COUNT 
            soup = BeautifulSoup(Main_Page)
#             Main_ID = ""
            # data = file.read()
            # file.close()
            table = soup.find("table", {"class" : "tableFile2"})
            rows = table.findAll('tr')
            flag = True
            print("Loop Start")
            for tr in rows:
                url = "http://www.sec.gov"
                if(flag == True):
                    xbrl = 'http://www.sec.gov'
                    cols = tr.findAll('td')
                    print(cols)
                    if cols:
                        interactive_lnk = cols[1].find('a', {"id" : "interactiveDataBtn"})
                        if interactive_lnk:
    #                       print(cols[3])
                            year = cols[3].contents[0]
                            link = cols[1].find('a').get('href')
    #                       print("short link is %s" % link)
                            url += link
    #                       print("URL is %s" % url)
                            Sub_Page = urllib2.urlopen(url).read()
                            soup1 = BeautifulSoup(Sub_Page)
                            tree = soup1.find('table', {"summary" : "Data Files"})
                            rows1 = tree.findAll('tr')
                            count = 0
                            count1 = 0
                            for tr1 in rows1:
                                if count == 1:
                                    cols1 = tr1.findAll('td')
                                    for td1 in cols1:
                                        if count1 == 2:
                                            yea = td1.find('a').contents[0]
                                            fir = yea.index('-')
                                            yea = yea[fir + 1:fir + 5]
                                            yearp[Ycounter]=yea
                                            kk = td1.find('a').get('href')
                                            xbrl += kk
                                            xbrl_URL[Ycounter]=xbrl
                                            if Ycounter==1:
                                                flag = False
                                            Ycounter=Ycounter+1
                                            
                                            print(kk)
                                        
                                        count1 = count1 + 1
                                count = count + 1
        print("Loop End")
            
        print("Nothing Find")
        xxx=0
        Current_Year=""
        Previous_Year=""
        Right_Dict = {}
        for yyy in yearp:
            list_PreURL_Data=[]
            checkExists = ticker_data_new.objects.filter(cik=CIK_Value, year=yyy)
            if not checkExists:
                Main_Page = urllib2.urlopen(xbrl_URL[xxx])
                Main_Page1=urllib2.urlopen(xbrl_URL[xxx])
                print("XML_page %s" %xbrl_URL[xxx])
                lis=ET.iterparse(Main_Page, ['start-ns'])
                for event, (name, value) in ET.iterparse(Main_Page, ['start-ns']):
#                     print name, ':', value
                    list_PreURL_Data.append(value)
                tree = ET.parse(Main_Page1)
                root = tree.getroot()
                list1 = ['Revenues', 'SalesRevenueNet', 'CostOfRevenue', 'ResearchAndDevelepmentExpense', 'SellingAndMarketingExpense', 'GeneralAndAdministrativeExpense', 'CostsAndExpenses', 'OperatingIncomeLoss', 'NonoperatingIncomeExpense', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityAndIncomeLossFromEquityMethodInvestments', 'IncomeTaxExpenseBenefit', 'IncomeLossFromContinuingOperations', 'IncomeLossFromDiscontinuedOperationsNetOfTax', 'NetIncomeLoss', 'EarningsPerShareBasicAbstract', 'IncomelossFromContinuingOperationsPerBasicshare', 'IncomelossfromdiscontinuedOperationsNetOfTaxPerBasicshare', 'EarningsPerShareDilutedAbstract', 'IncomeLossFromContinuingOperationsPerDilutedShare', 'IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedshare', 'EarningsPerShareDiluted', 'WeightedAverageNumberOfSharesOutstandingBasic', 'WeightedAverageNumberOfDilutedSharesOutstanding']
                list2 = ['IncreaseDecreaseInInventories', 'NetIncomeLoss', 'Depreciation', 'AmortizationOfIntangibleAssets', 'ShareBasedCompensation', 'DeferredIncomeTaxExpenseBenifit', 'MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments', 'OtherNonCashIncomeExpense', 'IncreaseDecreaseInAccountsReceivable', 'IncreaseDecreaseInInventories', 'IncreaseDecreaseInOtherCurrentAssets', 'IncreaseDecreaseInOtherNoncurrentAssets', 'IncreaseDecreaseInAccountsPayable', 'IncreaseDecreaseInDeferredRevenue', 'IncreaseDecreaseInOtherCurrentLiabilities', 'IncreaseDecreaseInOtherNoncurrentAssets', 'NetCashProvidedByUsedInOperatingActivities', 'PaymentToAcquireMarketingSecurities', 'ProceedsFromSaleAndMaturityOfMarketableSecurities', 'PaymentsToAcquireOtherInvestments', 'IncreaseDecreaseInCollateralHeldUnderSecuritiesLending', 'InvestmentsInReverseRepurchaseAgreements', 'AcquisitionsNetOfCashAcquiredAndPurchasesOfIntangiblesandOtherAssets', 'NetCashProvidedByUseInInvestingActivities', 'ExcessTaxBenifitFromShareBasedCompensationFinancingActivities', 'ProceedsFromDebtNetOfIssanceCosts', 'RepaymentsOfDebt', 'NetCashProvidedByUsedInFinancingActivities', 'EffectOfExchangeRateOnCashAndCashEquivalents', 'CashAndCashEquivalentPeriodIncreaseDecrease', 'CashAndCashEquivalentsAtCarryingValue', 'CashAndCashEquivalentsAtCarryingValue', 'IncomeTaxesPaid']
                list3 = ['Assets', 'CashAndCashEquivalentsAtCarryingValue', 'AvailableFroSaleSecuritiescurrent', 'CashCashEquivalentsAndShortTermInvestments', 'AccountsReceivableNetCurrent', 'InventoryNet', 'ReceivableUnderReverseRepurchaseAgreements', 'DeferredTaxAssetsNetcurrent', 'IncomeTaxesReceivable', 'PrepaidRevenueShareExpensesAndOtherAssetsCurrent', 'AssetsCurrent', 'PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent', 'OtherLongTermInvestments', 'PropertyPlantAndEquipmentNet', 'IntangibleAssetsNetExcludingGooldwill', 'Goodwill', 'Assets ', 'AccountsPayableCurrent ', 'ShortTermBorrowings', 'EmployeeRelatedLiabilitesCurrent', 'AccruedLiabilitesCurrent', 'DepositsReceivedForSecuritiesLoanedAtCarryingValue', 'DeferredRevenueCurrent', 'AccruedIncomeTaxesCurrent', 'LiabilitiesCurrent', 'LongTermDebtNoncurrent', 'DeferredRevenueNoncurrent', 'LiabilityForUncertainTaxPositionsNoncurrent', 'DeferredTaxLiabilitiesNoncurrent', 'OtherLiabilitiesNoncurrent', 'ConvertablePreferredStockNonRedeemableOrRedeemableIssuerOptionValue', 'AccumulatedOtherComprehensiveIncomeLossNetOfTax', 'RetainedEarningsAccumulatedDeficit', 'LiabilitiesAndStockholdersEquity', 'PreferredStockSharesOutstanding', 'CommonStockSharesOutstanding']
                list4 = ['StockholdersEquity', 'NetIncomeLoss', 'OhterComprehensiveIncomeLossNetOfTax', 'DividendsCommonStockCash', 'StockRepurchasedDuringPeriodValue', 'StockholdersEquity', 'CommonStockIncludingAdditionalPaidInCapitalMember', 'StockholdersEquity', 'StockIssuedDuringPeriodValueNewIssues', 'StockRepurchasedDuringPeriodValue', 'AdjustmentsToAdditionalPaidInCapitalShareBasedCompensationRequisiteServicePeriodRecognitionValue', 'AdjustmentToAdditionalPaidInCapitalIncomeTaxEffectFromShareBasedCompensationNet', 'ShareholdersEquityOther', 'ShareholdersEquity', 'ShareholdersEquity', 'ShareholdersEquity', 'NetIncomeLoss', 'DividendsCommonStockCash', 'StockRepurchasedDuringPeriodValue', 'ShareholdersEquity', 'ShareholdersEquity', 'OtherComprehensiveIncomeLossNetOfTax', 'ShareholdersEquity']
                TableIS[xxx] = IncomeStatement_Table(root, int(yyy), list1,list_PreURL_Data)
                TableCF[xxx] = CashFlowStatement_Table(root, int(yyy), list2,list_PreURL_Data)
                TableBS[xxx] = BalanceSheet_Table(root, int(yyy), list3,list_PreURL_Data)
                TableSE[xxx] = ShareholdersEquity_Table(root, int(yyy), list4,list_PreURL_Data)
                Right_Dict[0] = Gross_profit_margin()
                Right_Dict[1] = Operating_Profit_Margin()
                Right_Dict[2] = Quick_Ratio()
                Right_Dict[3] = Equity_Ratio()
                Right_Dict[4] = Return_on_Equity()
                Right_Dict[5] = Assets_Turnover()
                Right_Dict[6] = Debt_To_Equity()
                Right_Dict[7] = Inventory_Turnover()
                Right_Dict[8] = Long_Term_Debt_to_Capitalization_Ratio()
#                 Chart_Dict_IS[0] = 
                if xxx==0:
                    Current_Year=yyy
                if xxx==1:
                    Previous_Year=yyy
#                 keyRatioStrng[xxx] = "<table><tr><td>"+str(Right_Dict["GPM"])+"</td></tr><tr><td>"+str(Right_Dict["OPM"])+"</td></tr><tr><td>"+str(Right_Dict["QR"])+"</td></tr><tr><td>"+str(Right_Dict["ER"])+"</td></tr><tr><td>"+str(Right_Dict["RoE"])+"</td></tr><tr><td>"+str(Right_Dict["AT"])+"</td></tr><tr><td>"+str(Right_Dict["DTE"])+"</td></tr><tr><td>"+str(Right_Dict["IT"])+"</td></tr><tr><td>"+str(Right_Dict["LTDtCR"])+"</td></tr></table>"
                keyRatioStrng[xxx] = str(Right_Dict[0])+"|"+str(Right_Dict[1])+"|"+str(Right_Dict[2])+"|"+str(Right_Dict[3])+"|"+str(Right_Dict[4])+"|"+str(Right_Dict[5])+"|"+str(Right_Dict[6])+"|"+str(Right_Dict[7])+"|"+str(Right_Dict[8])
                historicalBarChart_BS = json.dumps([{'key': "Cumulative Return",'values': [{ "label" : "Cash and cash equivalents" ,"value" : float(Chart_Dict_BS["CashAndCashEquivalentsAtCarryingValue"]) if Chart_Dict_BS.has_key("CashAndCashEquivalentsAtCarryingValue") else 0} , { "label" : "Accounts receivable" , "value" : float(Chart_Dict_BS["AccountsReceivableNetCurrent"]) if Chart_Dict_BS.has_key("AccountsReceivableNetCurrent") else 0} , { "label" : "Inventories" , "value" : float(Chart_Dict_BS["InventoryNet"]) if Chart_Dict_BS.has_key("InventoryNet") else 0} , { "label" : "Deferred income taxes" , "value" : float(Chart_Dict_BS["DeferredTaxAssetsNetcurrent"]) if Chart_Dict_BS.has_key("DeferredTaxAssetsNetcurrent") else 0} , { "label" : "Total current assets" , "value" : float(Chart_Dict_BS["AssetsCurrent"]) if Chart_Dict_BS.has_key("AssetsCurrent") else 0} , { "label" : "Prepaid revenue share" , "value" : float(Chart_Dict_BS["PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent"]) if Chart_Dict_BS.has_key("PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent") else 0} , { "label" : "Non marketable equity investments" , "value" : float(Chart_Dict_BS["OtherLongTermInvestments"]) if Chart_Dict_BS.has_key("OtherLongTermInvestments") else 0}, { "label" : "Intangible assets" , "value" : float(Chart_Dict_BS["IntangibleAssetsNetExcludingGooldwill"]) if Chart_Dict_BS.has_key("IntangibleAssetsNetExcludingGooldwill") else 0}, { "label" : "Total assets" , "value" : float(Chart_Dict_BS["Assets"]) if Chart_Dict_BS.has_key("Assets") else 0}, { "label" : "Property and equipment" , "value" : float(Chart_Dict_BS["PropertyPlantAndEquipmentNet"]) if Chart_Dict_BS.has_key("PropertyPlantAndEquipmentNet") else 0}, { "label" : "Goodwill" , "value" : float(Chart_Dict_BS["Goodwill"]) if Chart_Dict_BS.has_key("Goodwill") else 0}]}])
#                 ChartStrng_BS[xxx] = str(Chart_Dict_BS["CashAndCashEquivalentsAtCarryingValue"])+"|"+str(Chart_Dict_BS["AccountsReceivableNetCurrent"])+"|"+str(Chart_Dict_BS["InventoryNet"])+"|"+str(Chart_Dict_BS["DeferredTaxAssetsNetcurrent"])+"|"+str(Chart_Dict_BS["IncomeTaxesReceivable"])+"|"+str(Chart_Dict_BS["AssetsCurrent"])+"|"+str(Chart_Dict_BS["PrepaidRevenueShareExpensesAndOtherAssetsNoncurrent"])+"|"+str(Chart_Dict_BS["OtherLongTermInvestments"])+"|"+str(Chart_Dict_BS["PropertyPlantAndEquipmentNet"])+"|"+str(Chart_Dict_BS["IntangibleAssetsNetExcludingGooldwill"])+"|"+str(Chart_Dict_BS["Goodwill"])+"|"+str(Chart_Dict_BS["Assets"])
                historicalBarChart_IS = json.dumps([{'key': "Cumulative Return",'values': [{ "label" : "Revenues" , "value" : float(Chart_Dict_IS["Revenues"]) if Chart_Dict_IS.has_key("Revenues") else 0} , { "label" : "Cost Of Revenue" ,"value" : float(Chart_Dict_IS["CostOfRevenue"]) if Chart_Dict_IS.has_key("CostOfRevenue") else 0} , { "label" : "Total Costs And Expenses" , "value" : float(Chart_Dict_IS["CostsAndExpenses"]) if Chart_Dict_IS.has_key("CostsAndExpenses") else 0} , { "label" : "Income from operations" , "value" : float(Chart_Dict_IS["OperatingIncomeLoss"]) if Chart_Dict_IS.has_key("OperatingIncomeLoss") else 0} , { "label" : "Net income from continuing operation" , "value" : float(Chart_Dict_IS["IncomeLossFromContinuingOperations"]) if Chart_Dict_IS.has_key("IncomeLossFromContinuingOperations") else 0}, { "label" : "Net Income Loss" , "value" : float(Chart_Dict_IS["NetIncomeLoss"]) if Chart_Dict_IS.has_key("NetIncomeLoss") else 0}]}])
#                 ChartStrng_IS[xxx] = str(ChartStrng_IS["Revenues"])+"|"+str(ChartStrng_IS["CostOfRevenue"])+"|"+str(ChartStrng_IS["CostsAndExpenses"])+"|"+str(ChartStrng_IS["OperatingIncomeLoss"])+"|"+str(ChartStrng_IS["IncomeLossFromContinuingOperations"])+"|"+str(Chart_Dict_BS["NetIncomeLoss"])
                historicalBarChart_CS = json.dumps([{'key': "Cumulative Return",'values': [{ "label" : "Net income" ,"value" : float(Chart_Dict_CS["NetIncomeLoss"]) if Chart_Dict_CS.has_key("NetIncomeLoss") else 0} , { "label" : "Depreciation and amortization of property" , "value" : float(Chart_Dict_CS["Depreciation"]) if Chart_Dict_CS.has_key("Depreciation") else 0} , { "label" : "Accounts payable" , "value" : float(Chart_Dict_CS["IncreaseDecreaseInAccountsPayable"]) if Chart_Dict_CS.has_key("IncreaseDecreaseInAccountsPayable") else 0} , { "label" : "Deferred revenue" , "value" : float(Chart_Dict_CS["IncreaseDecreaseInDeferredRevenue"]) if Chart_Dict_CS.has_key("IncreaseDecreaseInDeferredRevenue") else 0} , { "label" : "Net cash provided by investing activities" ,"value" : float(Chart_Dict_CS["NetCashProvidedByUseInInvestingActivities"]) if Chart_Dict_CS.has_key("NetCashProvidedByUseInInvestingActivities") else 0} , { "label" : "Net cash used in financing activities" , "value" : float(Chart_Dict_CS["NetCashProvidedByUsedInFinancingActivities"]) if Chart_Dict_CS.has_key("NetCashProvidedByUsedInFinancingActivities") else 0} , { "label" : "Net increase in cash and cash equivalents" , "value" : float(Chart_Dict_CS["CashAndCashEquivalentPeriodIncreaseDecrease"]) if Chart_Dict_CS.has_key("CashAndCashEquivalentPeriodIncreaseDecrease") else 0} , { "label" : "Cash and cash equivalents at beginning of period" , "value" : float(Chart_Dict_CS["CashAndCashEquivalentsAtCarryingValue"]) if Chart_Dict_CS.has_key("CashAndCashEquivalentsAtCarryingValue") else 0}, { "label" : "Cash and cash equivalents at end of period" , "value" : float(Chart_Dict_CS["CashAndCashEquivalentsAtCarryingValue"]) if Chart_Dict_CS.has_key("CashAndCashEquivalentsAtCarryingValue") else 0}]}])
#                 ChartStrng_CS[xxx] = str(Chart_Dict_CS["NetIncomeLoss"])+"|"+str(Chart_Dict_CS["Depreciation"])+"|"+str(Chart_Dict_CS["IncreaseDecreaseInAccountsPayable"])+"|"+str(Chart_Dict_CS["IncreaseDecreaseInDeferredRevenue"])+"|"+str(Chart_Dict_CS["NetCashProvidedByUseInInvestingActivities"])+"|"+str(Chart_Dict_CS["NetCashProvidedByUsedInFinancingActivities"])+"|"+str(Chart_Dict_CS["CashAndCashEquivalentPeriodIncreaseDecrease"])+"|"+str(Chart_Dict_CS["CashAndCashEquivalentsAtCarryingValue"])
                historicalBarChart_SE = json.dumps([{'key': "Cumulative Return",'values': [{ "label" : "Net Income" , "value" : float(Chart_Dict_SE["NetIncomeLoss"]) if Chart_Dict_SE.has_key("NetIncomeLoss") else 0} ,{ "label" : "Common stock re purchased" , "value" : float(Chart_Dict_SE["StockRepurchasedDuringPeriodValue"]) if Chart_Dict_SE.has_key("StockRepurchasedDuringPeriodValue") else 0} , { "label" : "Common stock issued" , "value" : float(Chart_Dict_SE["StockIssuedDuringPeriodValueNewIssues"]) if Chart_Dict_SE.has_key("StockIssuedDuringPeriodValueNewIssues") else 0}, { "label" : "Other net" , "value" : float(Chart_Dict_SE["ShareholdersEquityOther"]) if Chart_Dict_SE.has_key("ShareholdersEquityOther") else 0}]}])
#                 ChartStrng_SE[xxx] = str(ChartStrng_SE["NetIncomeLoss"])+"|"+str(ChartStrng_SE["StockRepurchasedDuringPeriodValue"])+"|"+str(ChartStrng_SE["ShareholdersEquityOther"])+"|"+str(ChartStrng_SE["StockIssuedDuringPeriodValueNewIssues"])
                modl = ticker_data_new(cik=CIK_Value, keyratios=keyRatioStrng[xxx] , xbrl_bs=TableBS[xxx], xbrl_is=TableIS[xxx], xbrl_cf=TableCF[xxx], xbrl_se=TableSE[xxx], year=yyy,chart_bs=historicalBarChart_BS, chart_is=historicalBarChart_IS, chart_cf=historicalBarChart_CS, chart_se=historicalBarChart_SE)
                modl.save(force_insert=True, force_update=False, using=None, update_fields=None)
                xxx=xxx+1
            else:
                TableBS[xxx] = checkExists[0].xbrl_bs
                TableIS[xxx] = checkExists[0].xbrl_is
                TableCF[xxx] = checkExists[0].xbrl_cf
                TableSE[xxx] = checkExists[0].xbrl_se
                keyRatioStrng[xxx] = checkExists[0].keyratios
                 
                Right_Dict = keyRatioStrng[xxx].split('|')
                historicalBarChart_BS=checkExists[0].chart_bs
                historicalBarChart_IS=checkExists[0].chart_is
                historicalBarChart_SE=checkExists[0].chart_se
                historicalBarChart_CS=checkExists[0].chart_cf
                if xxx==0:
                    Current_Year=checkExists[0].year
                if xxx==1:
                    Previous_Year=checkExists[0].year
                xxx=xxx+1
             
#         print("TableIS=%s"%TableIS)
#         print("TableCF=%s"%TableCF)
#         print("TableBS=%s"%TableBS)
#         print("TableSE=%s"%TableSE)

#         cont = Context({'Current_Year' :  Current_Year,'Previous_Year' :  Previous_Year,'BS_statement1' :  TableBS[0], 'IN_statement1' :  TableIS[0], 'CF_statement1' :  TableCF[0], 'SH_Equity1' :  TableSE[0], 'KEY_RatiosBookMark1' : keyRatioStrng[0], 'BS_statement2' :  TableBS[1], 'IN_statement2' :  TableIS[1], 'CF_statement2' :  TableCF[1], 'SH_Equity2' :  TableSE[1], 'KEY_RatiosBookMark2' : keyRatioStrng[1], 'GPM_A' : Right_Dict[0], 'OPM_A' : Right_Dict[1], 'QR_A' : Right_Dict[2], 'ER_A' : Right_Dict[3], 'ROE_A' : Right_Dict[4], 'AT_A' : Right_Dict[5], 'DTE_A' : Right_Dict[6], 'IT_A' : Right_Dict[7], 'LDT_A' : Right_Dict[8], 'HST_BalanceSheet' : historicalBarChart_BS,'HST_IncomeStatement' : historicalBarChart_IS,'HST_ShareHolder' :historicalBarChart_SE,'HST_Cashflow' : historicalBarChart_CS})
#         xt4 = templ.render(cont)
#         resp.write(xt4)
#     return resp
        return render_to_response("polls/Statements.html",
                                  {'Current_Year' :  Current_Year,
                                   'Previous_Year' :  Previous_Year,
                                   'BS_statement1' :  TableBS[0],
                                   'IN_statement1' :  TableIS[0],
                                   'CF_statement1' :  TableCF[0],
                                   'SH_Equity1' :  TableSE[0],
                                   'KEY_RatiosBookMark1' : keyRatioStrng[0],
                                   'BS_statement2' :  TableBS[1],
                                   'IN_statement2' :  TableIS[1],
                                   'CF_statement2' :  TableCF[1],
                                   'SH_Equity2' :  TableSE[1],
                                   'KEY_RatiosBookMark2' : keyRatioStrng[1],
                                   'GPM_A' : Right_Dict[0],
                                   'OPM_A' : Right_Dict[1],
                                   'QR_A' : Right_Dict[2],
                                   'ER_A' : Right_Dict[3],
                                   'ROE_A' : Right_Dict[4],
                                   'AT_A' : Right_Dict[5],
                                   'DTE_A' : Right_Dict[6],
                                   'IT_A' : Right_Dict[7], 'LDT_A' : Right_Dict[8],
                                   'HST_BalanceSheet' : historicalBarChart_BS,
                                   'HST_IncomeStatement' : historicalBarChart_IS,
                                   'HST_ShareHolder' :historicalBarChart_SE,
                                   'HST_Cashflow' : historicalBarChart_CS},
            context_instance=RequestContext(request)
            )                 

def DBcheck(request):
#     modl=ticker_data(cik="1238987",xbrl="aksdjlasfjhalkshflahsl",year="2012")
#     modl.save(force_insert=True, force_update=False, using=None, update_fields=None)
#     modl1=ticker_data(cik="1238987",xbrl="aksdjlasfjhalkshflahsl",year="2013")
#     modl.save(force_insert=True, force_update=False, using=None, update_fields=None)  
    temp = ticker_data.objects.all()
    stringg = ""
    for t in temp:
        stringg += t.xbrl + "<br/>"
    return HttpResponse("this is DB check!  .." + stringg)

@csrf_protect
def Statements(request):
    template = loader.get_template('polls/Statements.html')
    c = RequestContext(request, {})
    return HttpResponse(template.render(c))

@csrf_protect
def GetCompanyCache(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        result = companies.objects.filter(company_name__istartswith=q)[:10]
        
        results = []
        for res in result:
            drug_json = {}
            drug_json['id'] = res.cik
            drug_json['label'] = res.company_name
            drug_json['value'] = res.company_name
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
